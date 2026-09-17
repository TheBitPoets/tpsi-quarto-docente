"""Regression checks for the hybrid lesson formatter."""
import importlib.util
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("lesson_formatter", ROOT / "scripts/format_tpsi4_lessons.py")
formatter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(formatter)


class LessonFormattingTests(unittest.TestCase):
    def test_lessons_are_balanced_and_already_normalized(self):
        self.assertGreater(len(formatter.DEFAULT_LESSONS), 0)
        for path in formatter.DEFAULT_LESSONS:
            with self.subTest(lesson=path.name):
                text = path.read_text(encoding="utf-8")
                self.assertEqual(formatter.validation_errors(text), [])
                self.assertEqual(formatter.normalize(text), text)

    def test_every_lesson_has_visible_definition_panels(self):
        for path in formatter.DEFAULT_LESSONS:
            with self.subTest(lesson=path.name):
                text = path.read_text(encoding="utf-8")
                self.assertIn('<!-- definition -->', text)
                self.assertEqual(formatter.validation_errors(text), [])

    def test_definition_template_and_marker_errors_are_detected(self):
        panel = ('<!-- definition -->\n<table align="center">\n<tr><td>\n'
                 '&#10071; <strong>Importante</strong>\n'
                 '<p align="justify">A <strong>term</strong> has a meaning.</p>\n'
                 '</td></tr>\n</table>\n<!-- /definition -->')
        valid = '# Lesson\n\n' + panel + '\n'
        self.assertEqual(formatter.validation_errors(valid), [])
        self.assertEqual(formatter.normalize(valid), valid)
        invalid = [
            panel.replace('align="center"', 'align="left"'),
            panel.replace('align="justify"', 'align="left"'),
            panel.replace('<strong>term</strong>', 'term'),
            panel.replace('<!-- /definition -->', ''),
            panel.replace('<!-- definition -->', ''),
            panel.replace('<!-- definition -->', '<!-- definition -->\n<!-- definition -->'),
            panel.replace('<p align="justify">', '<details><p align="justify">').replace('</p>', '</p></details>'),
        ]
        for sample in invalid:
            with self.subTest(panel=sample):
                self.assertTrue(formatter.validation_errors('# Lesson\n\n' + sample))
        code_example = '# Lesson\n\n```html\n' + invalid[0] + '\n```\n'
        self.assertEqual(formatter.validation_errors(code_example), [])

    def test_orientation_uses_the_reference_icons_and_table(self):
        for path in formatter.DEFAULT_LESSONS:
            text = path.read_text(encoding="utf-8")
            panel = text.split("<!-- visual-orientation -->", 1)[1].split("</table>", 1)[0]
            self.assertIn('<table align="center">', panel)
            self.assertIn('<summary>&#129517; <strong>Orientamento della sezione</strong></summary>', panel)
            for icon, label in [(128506, "Contesto"), (128736, "Prerequisiti"),
                                (127919, "Obiettivi"), (128257, "Richiamo"),
                                (128064, "Anticipazione"), (10145, "Prossimo passo"),
                                (128279, "Rimando")]:
                self.assertIn(f'&#{icon};</span> {label}:</strong>', panel)
            self.assertIn('href="#fonti-e-note-di-revisione"', panel)
            self.assertEqual(panel.count('<p align="justify">'), 7)

    def test_code_and_example_headings_remain_literal(self):
        code = "```c\n#include <stdio.h>\nif (a < b && c > 0) puts(\"<p>\");\n```"
        sample = '# Lesson\n\nTesto con **enfasi** e `a < b && c > 0`.\n\n' + code + '\n\n```text\n# Example README\n## Section\n```\n'
        result = formatter.normalize(sample)
        self.assertIn(code, result)
        self.assertIn('<code>a &lt; b &amp;&amp; c &gt; 0</code>', result)
        self.assertIn('<strong>enfasi</strong>', result)
        self.assertEqual(formatter.validation_errors(result), [])
        self.assertTrue(formatter.validation_errors('# One\n\n# Two\n'))

    def test_existing_multiline_html_is_preserved(self):
        paragraph = '<p align="justify">\nTesto <strong>esistente</strong>.\n</p>'
        pre = '<pre lang="c"><code>x &lt; 4</code></pre>'
        sample = '# Lesson\n\n' + paragraph + '\n\n' + pre + '\n\nNuovo paragrafo.\n'
        result = formatter.normalize(sample)
        self.assertIn(paragraph, result)
        self.assertIn(pre, result)
        self.assertIn('<p align="justify">Nuovo paragrafo.</p>', result)
        self.assertEqual(formatter.normalize(result), result)
        self.assertEqual(formatter.validation_errors(result), [])

    def test_table_links_and_list_order_survive_conversion(self):
        sample = '# Lesson\n\n| API | Fonte |\n| --- | --- |\n| `fork()` | [Guida](guide.md#fork) |\n\n1. prima\n2. seconda\n'
        result = formatter.normalize(sample)
        self.assertIn('<table align="center">', result)
        self.assertIn('<td><code>fork()</code></td>', result)
        self.assertIn('<a href="guide.md#fork">Guida</a>', result)
        self.assertIn('<ol>\n  <li>prima</li>\n  <li>seconda</li>\n</ol>', result)
        self.assertEqual(formatter.validation_errors(result), [])


if __name__ == "__main__":
    unittest.main()
