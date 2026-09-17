#!/usr/bin/env python3
"""Normalize TPSI4 lesson prose to the repository hybrid HTML/Markdown style.

Adapted from TheBitPoets/tpsi-quinto-docente/scripts/format_tpsi5_lessons.py
(reference read on 2026-09-14).

Headings and fenced code remain Markdown. Prose, simple lists, blockquotes and
pipe tables become GitHub-compatible HTML. Existing HTML blocks are preserved.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from html.parser import HTMLParser


ROOT = Path(__file__).resolve().parents[1]
LESSON_DIR = ROOT / "content" / "tpsi_quarto"
DEFAULT_LESSONS = tuple(
    path
    for path in sorted(LESSON_DIR.glob("[0-9][0-9]_*.md"))
)

FENCE_RE = re.compile(r"^\s*(```|~~~)")
HEADING_RE = re.compile(r"^#{1,6}\s")
UL_RE = re.compile(r"^-\s+(.*)$")
OL_RE = re.compile(r"^\d+[.)]\s+(.*)$")
TABLE_SEPARATOR_RE = re.compile(
    r"^\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?\s*$"
)
RAW_BLOCK_TAGS = ("p", "table", "details", "blockquote", "div", "ul", "ol", "pre")
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


class BalanceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[str] = []
        self.errors: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag not in VOID_TAGS:
            self.stack.append(tag)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        return

    def handle_endtag(self, tag: str) -> None:
        if not self.stack:
            self.errors.append(f"closing </{tag}> without opening tag")
            return
        opened = self.stack.pop()
        if opened != tag:
            self.errors.append(f"closing </{tag}> while <{opened}> is open")


def html_outside_fences(content: str) -> str:
    output: list[str] = []
    marker: str | None = None
    for line in content.splitlines():
        fence = FENCE_RE.match(line)
        if fence:
            current = fence.group(1)
            marker = None if marker == current else current
            continue
        if marker is None:
            if not HEADING_RE.match(line):
                output.append(line)
    return "\n".join(output)


def validation_errors(content: str) -> list[str]:
    errors: list[str] = []
    visible_lines = []
    marker = None
    for line in content.splitlines():
        fence = FENCE_RE.match(line)
        if fence:
            current = fence.group(1)
            marker = None if marker == current else current
        elif marker is None:
            visible_lines.append(line)
    if marker:
        errors.append("unclosed fenced code block")
    if sum(line.startswith("# ") for line in visible_lines) != 1:
        errors.append("the document must contain exactly one level-1 heading")
    visible = html_outside_fences(content)
    parser = BalanceParser()
    parser.feed(visible)
    errors.extend(parser.errors)
    errors.extend(f"unclosed <{tag}>" for tag in reversed(parser.stack))
    definition_open = False
    definition_parts: list[str] = []
    for line in visible.splitlines():
        if line.strip() == "<!-- definition -->":
            if definition_open:
                errors.append("nested definition panel")
            definition_open = True
            definition_parts = []
        elif line.strip() == "<!-- /definition -->":
            if not definition_open:
                errors.append("closing definition marker without opening marker")
                continue
            panel = "\n".join(definition_parts).strip()
            header = '<table align="center">\n<tr><td>\n&#10071; <strong>Importante</strong>\n'
            footer = '\n</td></tr>\n</table>'
            if not panel.startswith(header) or not panel.endswith(footer):
                errors.append("definition must use the centered Importante template")
            else:
                body = panel[len(header):-len(footer)]
                if '<p align="justify">' not in body or '<strong>' not in body:
                    errors.append("definition needs justified prose and a bold term")
                if '<table' in body or '<details' in body:
                    errors.append("definition must remain visible without nested tables")
            definition_open = False
        elif definition_open:
            definition_parts.append(line)
    if definition_open:
        errors.append("unclosed definition marker")
    if re.search(r'Definizione:\s*</strong>', visible):
        errors.append("obsolete definition panel: use the Importante template")
    return errors


def inline_html(text: str) -> str:
    """Convert the small Markdown-inline subset used by these lessons."""
    protected: list[str] = []

    def protect(match: re.Match[str]) -> str:
        value = match.group(1).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        protected.append(f"<code>{value}</code>")
        return f"\x00{len(protected) - 1}\x00"

    text = re.sub(r"`([^`\n]+)`", protect, text)
    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"<(https?://[^>]+)>", r'<a href="\1">\1</a>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)

    for index, value in enumerate(protected):
        text = text.replace(f"\x00{index}\x00", value)
    return text


def split_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def render_table(rows: list[str]) -> list[str]:
    headers = split_table_row(rows[0])
    body = [split_table_row(row) for row in rows[2:]]
    output = ["<table align=\"center\">", "<thead>", "<tr>"]
    output.extend(f"<th>{inline_html(cell)}</th>" for cell in headers)
    output.extend(["</tr>", "</thead>", "<tbody>"])
    for row in body:
        output.append("<tr>")
        output.extend(f"<td>{inline_html(cell)}</td>" for cell in row)
        output.append("</tr>")
    output.extend(["</tbody>", "</table>"])
    return output


def raw_block_tag(line: str) -> str | None:
    stripped = line.lstrip().lower()
    for tag in RAW_BLOCK_TAGS:
        if re.match(rf"<{tag}(?=[\s>])", stripped):
            return tag
    return None


def is_boundary(lines: list[str], index: int) -> bool:
    line = lines[index]
    if not line.strip():
        return True
    if FENCE_RE.match(line) or HEADING_RE.match(line) or line.strip() == "---":
        return True
    if line.lstrip().startswith("<!--") or line.lstrip().startswith("<"):
        return True
    if UL_RE.match(line) or OL_RE.match(line) or line.startswith(">"):
        return True
    if index + 1 < len(lines) and line.lstrip().startswith("|") and TABLE_SEPARATOR_RE.match(lines[index + 1]):
        return True
    return False


def normalize(content: str) -> str:
    lines = content.splitlines()
    output: list[str] = []
    index = 0

    while index < len(lines):
        line = lines[index]

        fence = FENCE_RE.match(line)
        if fence:
            marker = fence.group(1)
            output.append(line)
            index += 1
            while index < len(lines):
                output.append(lines[index])
                closing = lines[index].lstrip().startswith(marker)
                index += 1
                if closing:
                    break
            continue

        if line.lstrip().startswith("<!--"):
            output.append(line)
            index += 1
            while "-->" not in output[-1] and index < len(lines):
                output.append(lines[index])
                index += 1
            continue

        tag = raw_block_tag(line)
        if tag:
            depth = len(re.findall(rf"<{tag}(?=[\s>])", line, re.I)) - line.lower().count(f"</{tag}>")
            output.append(line)
            index += 1
            while depth > 0 and index < len(lines):
                current = lines[index]
                lower = current.lower()
                depth += len(re.findall(rf"<{tag}(?=[\s>])", lower)) - lower.count(f"</{tag}>")
                output.append(current)
                index += 1
            continue

        if not line.strip() or HEADING_RE.match(line) or line.strip() == "---" or line.lstrip().startswith("<"):
            output.append(line)
            index += 1
            continue

        if index + 1 < len(lines) and line.lstrip().startswith("|") and TABLE_SEPARATOR_RE.match(lines[index + 1]):
            rows = [line, lines[index + 1]]
            index += 2
            while index < len(lines) and lines[index].lstrip().startswith("|"):
                rows.append(lines[index])
                index += 1
            output.extend(render_table(rows))
            continue

        unordered = UL_RE.match(line)
        ordered = OL_RE.match(line)
        if unordered or ordered:
            pattern = UL_RE if unordered else OL_RE
            tag_name = "ul" if unordered else "ol"
            output.append(f"<{tag_name}>")
            while index < len(lines):
                match = pattern.match(lines[index])
                if not match:
                    break
                output.append(f"  <li>{inline_html(match.group(1))}</li>")
                index += 1
            output.append(f"</{tag_name}>")
            continue

        if line.startswith(">"):
            quotes: list[str] = []
            while index < len(lines) and lines[index].startswith(">"):
                quotes.append(lines[index][1:].lstrip())
                index += 1
            quote_text = " ".join(part for part in quotes if part)
            output.extend([
                "<blockquote>",
                f'<p align="justify">{inline_html(quote_text)}</p>',
                "</blockquote>",
            ])
            continue

        paragraph = [line.strip()]
        index += 1
        while index < len(lines) and not is_boundary(lines, index):
            paragraph.append(lines[index].strip())
            index += 1
        output.append(f'<p align="justify">{inline_html(" ".join(paragraph))}</p>')

    return "\n".join(output).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="rewrite lessons in place")
    mode.add_argument("--check", action="store_true", help="fail if normalization would change files")
    parser.add_argument("files", nargs="*", type=Path)
    args = parser.parse_args()

    paths = tuple(args.files) or DEFAULT_LESSONS
    changed: list[Path] = []
    invalid = False
    for raw_path in paths:
        path = raw_path if raw_path.is_absolute() else ROOT / raw_path
        before = path.read_text(encoding="utf-8")
        after = normalize(before)
        candidate = after if args.write else before
        for error in validation_errors(candidate):
            invalid = True
            print(f"{path.relative_to(ROOT)}: {error}")
        if before == after:
            continue
        changed.append(path)
        if args.write:
            path.write_text(after, encoding="utf-8", newline="\n")

    for path in changed:
        print(path.relative_to(ROOT))
    return 1 if invalid or (args.check and changed) else 0


if __name__ == "__main__":
    raise SystemExit(main())
