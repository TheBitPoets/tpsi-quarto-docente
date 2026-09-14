#!/usr/bin/env python3
"""Build standalone TPSI4 SVGs. Adapted from the TPSI5 scene/defs workflow.

Only Python's standard library is required. Sources and generated SVGs are
versioned; --check never writes files. See assets/tpsi4/visual-system/README.md.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "tpsi4"
VISUAL_ROOT = ASSETS / "visual-system"
SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)


def tag(name: str) -> str:
    return f"{{{SVG_NS}}}{name}"


def validate_svg(root: ET.Element) -> None:
    """Catch unresolved symbols, duplicate IDs and nonlocal dependencies."""
    ids = [node.attrib["id"] for node in root.iter() if "id" in node.attrib]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate SVG ID")
    known = set(ids)
    for element in ("title", "desc"):
        node = root.find(tag(element))
        if node is None or not (node.text or "").strip():
            raise ValueError(f"missing accessible {element}")
    if root.get("role") != "img":
        raise ValueError("missing image role")
    labelled = root.get("aria-labelledby", "").split()
    if not labelled or any(value not in known for value in labelled):
        raise ValueError("invalid aria-labelledby")
    for node in root.iter():
        if node.tag in {tag("script"), tag("foreignObject"), tag("image")}:
            raise ValueError("only static vector elements are supported")
        for key, value in node.attrib.items():
            if key.lower().startswith("on"):
                raise ValueError("event handler in SVG")
            if key == "href" or key.endswith("}href"):
                if not value.startswith("#") or value[1:] not in known:
                    raise ValueError(f"unknown or external reference: {value}")
                if node.tag == tag("use") and not value.startswith("#tpsi-"):
                    raise ValueError(f"use must reference a TPSI component: {value}")
        source = " ".join(node.attrib.values()) + (node.text or "")
        if "@import" in source:
            raise ValueError("external CSS import")
        for value in re.findall(r"url\((.*?)\)", source):
            value = value.strip(" \"'")
            if not value.startswith("#") or value[1:] not in known:
                raise ValueError(f"unresolved paint/marker: {value}")


def render_scene(path: Path, definitions: list[ET.Element], tokens: dict,
                 assets: Path = ASSETS) -> tuple[Path, bytes]:
    raw = path.read_text(encoding="utf-8")
    values = {**tokens["colors"], **tokens["typography"]}
    def replace(match: re.Match) -> str:
        key = match.group(1)
        if key not in values:
            raise ValueError(f"unknown visual token: {key}")
        return str(values[key])
    root = ET.fromstring(re.sub(r"\{\{(\w+)\}\}", replace, raw))
    output_value = root.attrib.pop("data-output", "")
    if not output_value:
        raise ValueError(f"{path.name}: missing data-output")
    output = (path.parent / output_value).resolve()
    allowed = assets.resolve()
    if output.parent not in {allowed, allowed / "visual-system" / "catalog"}:
        raise ValueError(f"output outside generated asset directories: {output}")
    if output.suffix != ".svg":
        raise ValueError("output must be SVG")
    if root.get("viewBox") != f"0 0 {tokens['canvas']['width']} {tokens['canvas']['height']}":
        raise ValueError("scene must use the canonical canvas")
    placeholders = [d for d in root.findall(tag("defs"))
                    if d.get("id") == "visual-kit-components"]
    if len(placeholders) != 1:
        raise ValueError("expected one visual-kit-components placeholder")
    placeholders[0].attrib.pop("id")
    placeholders[0].extend(deepcopy(definitions))
    # Definitions can use the same visual tokens as the scene.
    root = ET.fromstring(re.sub(r"\{\{(\w+)\}\}", replace, ET.tostring(root, encoding="unicode")))
    validate_svg(root)
    ET.indent(root, space="  ")
    return output, ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"


def planned_outputs() -> list[tuple[Path, bytes]]:
    tokens = json.loads((VISUAL_ROOT / "tokens.json").read_text(encoding="utf-8"))
    library = ET.parse(VISUAL_ROOT / "components.svg").getroot()
    defs = library.find(tag("defs"))
    if defs is None:
        raise ValueError("components.svg has no definitions")
    scenes = sorted((VISUAL_ROOT / "scenes").glob("*.scene.svg"))
    if not scenes:
        raise ValueError("no scenes")
    outputs = [render_scene(path, list(defs), tokens) for path in scenes]
    targets = [path for path, _ in outputs]
    if len(targets) != len(set(targets)):
        raise ValueError("two scenes declare the same output")
    return outputs


def build(check: bool = False) -> int:
    outputs = planned_outputs()  # Validate every source before writing any file.
    stale = []
    for path, payload in outputs:
        if check:
            if not path.is_file() or path.read_bytes() != payload:
                stale.append(path.relative_to(ROOT).as_posix())
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(payload)
    if stale:
        print("SVG da rigenerare:\n" + "\n".join(stale), file=sys.stderr)
        return 1
    print(f"OK: {len(outputs)} SVG {'aggiornati' if check else 'generati'}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        return build(args.check)
    except (ValueError, OSError, ET.ParseError) as error:
        print(f"Errore Visual System: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
