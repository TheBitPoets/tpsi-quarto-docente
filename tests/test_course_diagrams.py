"""Standalone checks for the TPSI4 visual system; no platform checkout needed."""
from copy import deepcopy
import html
import importlib.util
import json
from pathlib import Path
import re
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("tpsi4_diagrams", ROOT / "scripts/build_course_diagrams.py")
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


class VisualSystemTests(unittest.TestCase):
    def test_generated_assets_are_current(self):
        for output, expected in builder.planned_outputs():
            with self.subTest(output=output.name):
                self.assertEqual(output.read_bytes(), expected)
                builder.validate_svg(ET.fromstring(expected))

    def test_inventory_and_catalogs_cover_the_library(self):
        kit = builder.VISUAL_ROOT
        library = ET.parse(kit / "components.svg").getroot()
        symbols = {node.get("id") for node in library.iter(builder.tag("symbol"))}
        inventory = json.loads((kit / "component-inventory.json").read_text(encoding="utf-8"))["components"]
        self.assertEqual(symbols, {item["id"] for item in inventory})
        self.assertEqual(len(inventory), len(symbols))
        shown = set()
        for path in (kit / "scenes").glob("catalog-*.scene.svg"):
            shown.update(node.get("href")[1:] for node in ET.parse(path).getroot().iter(builder.tag("use")))
        self.assertEqual(shown, symbols)

    def test_figures_are_linked_in_the_declared_sections(self):
        figures = json.loads((builder.VISUAL_ROOT / "figure-index.json").read_text(encoding="utf-8"))["figures"]
        self.assertEqual(len(figures), len({f["id"] for f in figures}))
        self.assertEqual(len(figures), len({f["output"] for f in figures}))
        self.assertEqual(
            {f["scene"] for f in figures},
            {p.relative_to(ROOT).as_posix() for p in (builder.VISUAL_ROOT / "scenes").glob("*.scene.svg")
             if not p.name.startswith("catalog-")},
        )
        for item in figures:
            with self.subTest(figure=item["id"]):
                text = (ROOT / item["lesson"]).read_text(encoding="utf-8")
                heading = "## " + item["section"] + "\n"
                self.assertEqual(text.count(heading), 1)
                visible = re.sub(r"```.*?```", "", text, flags=re.S)
                section = visible.split(heading, 1)[1].split("\n## ", 1)[0]
                marker = "<!-- figure:" + item["id"] + " -->"
                self.assertEqual(text.count(marker), 1)
                self.assertIn(marker, section)
                self.assertIn('alt="' + html.escape(item["alt"], quote=True) + '"', section)
                self.assertIn('src="../../' + item["output"] + '"', section)
                self.assertIn(html.escape(item["caption"]), section)
                self.assertTrue((ROOT / item["output"]).is_file())
                scene = ET.parse(ROOT / item["scene"]).getroot()
                uses = {n.get("href")[1:] for n in scene.iter(builder.tag("use"))}
                self.assertEqual(set(item["components"]), uses)
                target = (ROOT / item["scene"]).parent / scene.get("data-output")
                self.assertEqual(target.resolve(), (ROOT / item["output"]).resolve())

    def test_rejects_missing_symbols_external_refs_and_duplicate_ids(self):
        sample = ET.fromstring(builder.planned_outputs()[0][1])
        use = ET.SubElement(sample, builder.tag("use"), {"href": "#tpsi-absent"})
        with self.assertRaisesRegex(ValueError, "unknown or external"):
            builder.validate_svg(sample)
        use.set("href", "https://example.invalid/image.svg")
        with self.assertRaisesRegex(ValueError, "unknown or external"):
            builder.validate_svg(sample)
        sample.remove(use)
        ET.SubElement(sample, builder.tag("g"), {"id": "scene-title"})
        with self.assertRaisesRegex(ValueError, "duplicate"):
            builder.validate_svg(sample)

    def test_output_cannot_overwrite_source_or_escape_asset_directory(self):
        kit = builder.VISUAL_ROOT
        tokens = json.loads((kit / "tokens.json").read_text(encoding="utf-8"))
        defs = list(ET.parse(kit / "components.svg").getroot().find(builder.tag("defs")))
        source = ET.parse(next((kit / "scenes").glob("*.scene.svg"))).getroot()
        with tempfile.TemporaryDirectory() as temp:
            assets = Path(temp) / "assets"
            scene_dir = assets / "visual-system" / "scenes"
            scene_dir.mkdir(parents=True)
            path = scene_dir / "probe.scene.svg"
            for output in ["../../../../escape.svg", "../components.svg", "../../probe.json"]:
                with self.subTest(output=output):
                    modified = deepcopy(source)
                    modified.set("data-output", output)
                    ET.ElementTree(modified).write(path, encoding="utf-8")
                    with self.assertRaises(ValueError):
                        builder.render_scene(path, defs, tokens, assets)

    def test_authoring_document_links(self):
        paths = [ROOT / "doc/VISUAL_AUDIT.md",
                 builder.VISUAL_ROOT / "README.md",
                 ROOT / "content/tpsi_quarto/STYLE_GUIDE.md"]
        for path in paths:
            text = re.sub(r"```.*?```", "", path.read_text(encoding="utf-8"), flags=re.S)
            for link in re.findall(r"\]\(([^)]+)\)", text):
                if link.startswith(("https://", "http://")):
                    continue
                relative, _, anchor = link.partition("#")
                target = (path.parent / relative).resolve()
                with self.subTest(path=path.name, link=link):
                    self.assertTrue(target.exists())
                    if anchor:
                        body = re.sub(r"```.*?```", "", target.read_text(encoding="utf-8"), flags=re.S)
                        headings = re.findall(r"^#+ (.+)$", body, re.M)
                        slugs = [re.sub(r"[^\w\- ]", "", h.lower()).replace(" ", "-") for h in headings]
                        self.assertIn(anchor, slugs)

    def test_token_changes_propagate_to_rendered_assets(self):
        kit = builder.VISUAL_ROOT
        tokens = json.loads((kit / "tokens.json").read_text(encoding="utf-8"))
        defs = list(ET.parse(kit / "components.svg").getroot().find(builder.tag("defs")))
        scene = next((kit / "scenes").glob("*.scene.svg"))
        _, before = builder.render_scene(scene, defs, tokens)
        tokens["colors"]["canvas"] = "#010203"
        tokens["colors"]["process"] = "#123456"
        _, after = builder.render_scene(scene, defs, tokens)
        self.assertNotEqual(before, after)
        self.assertIn(b"#010203", after)
        self.assertIn(b"#123456", after)
        self.assertNotIn(b"{{", after)


if __name__ == "__main__":
    unittest.main()
