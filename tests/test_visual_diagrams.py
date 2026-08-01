from __future__ import annotations

import re
from pathlib import Path
import xml.etree.ElementTree as ET

import pytest


ROOT = Path(__file__).resolve().parents[1]
CONTENT_ROOT = ROOT / "content" / "tpsi_quarto"
DIAGRAM_ROOT = CONTENT_ROOT / "assets" / "diagrams"
SVG_NS = "http://www.w3.org/2000/svg"

EXPECTED_DIAGRAMS = {
    "01-process-lifecycle.svg",
    "01-execution-models.svg",
    "02-producer-consumer-buffer.svg",
    "02-deadlock-cycle.svg",
    "03-requirements-traceability.svg",
    "04-architecture-layers.svg",
}

INTEGRATED_REFERENCES = {
    "01_PROCESSI_E_CONCORRENZA.md": {
        "assets/diagrams/01-process-lifecycle.svg",
        "assets/diagrams/01-execution-models.svg",
    },
    "02_COMUNICAZIONE_E_SINCRONIZZAZIONE.md": {
        "assets/diagrams/02-producer-consumer-buffer.svg",
        "assets/diagrams/02-deadlock-cycle.svg",
    },
    "03_REQUISITI_SOFTWARE.md": {
        "assets/diagrams/03-requirements-traceability.svg",
    },
    "04_DOCUMENTAZIONE_VERSIONAMENTO.md": {
        "assets/diagrams/04-architecture-layers.svg",
    },
}


@pytest.mark.parametrize("filename", sorted(EXPECTED_DIAGRAMS))
def test_svg_is_accessible_self_contained_and_valid(filename: str) -> None:
    path = DIAGRAM_ROOT / filename
    assert path.is_file(), path

    raw = path.read_text(encoding="utf-8")
    root = ET.fromstring(raw)

    assert root.tag == f"{{{SVG_NS}}}svg"
    assert root.get("role") == "img"

    labelled_by = root.get("aria-labelledby", "").split()
    assert labelled_by, f"{filename}: aria-labelledby mancante"

    title = root.find(f"{{{SVG_NS}}}title")
    desc = root.find(f"{{{SVG_NS}}}desc")
    assert title is not None and (title.text or "").strip()
    assert desc is not None and len((desc.text or "").strip()) >= 40
    assert title.get("id") in labelled_by
    assert desc.get("id") in labelled_by

    assert "<script" not in raw.lower()
    assert "http://" not in raw.replace("http://www.w3.org/2000/svg", "")
    assert "https://" not in raw
    assert "@import" not in raw.lower()
    assert "font-family" in raw


def test_expected_diagram_set_has_no_accidental_extra_assets() -> None:
    actual = {path.name for path in DIAGRAM_ROOT.glob("*.svg")}
    assert actual == EXPECTED_DIAGRAMS


@pytest.mark.parametrize("markdown_name", sorted(INTEGRATED_REFERENCES))
def test_markdown_references_existing_diagrams_and_text_fallback(markdown_name: str) -> None:
    markdown_path = CONTENT_ROOT / markdown_name
    text = markdown_path.read_text(encoding="utf-8")

    references = set(re.findall(r"\]\((assets/diagrams/[^)]+\.svg)\)", text))
    assert INTEGRATED_REFERENCES[markdown_name] <= references

    for relative in INTEGRATED_REFERENCES[markdown_name]:
        assert (CONTENT_ROOT / relative).is_file(), relative

    assert text.count("<details>") >= len(INTEGRATED_REFERENCES[markdown_name])
    assert text.count("Versione testuale") >= len(INTEGRATED_REFERENCES[markdown_name])


def test_every_integrated_image_has_meaningful_alt_text() -> None:
    for markdown_name in INTEGRATED_REFERENCES:
        text = (CONTENT_ROOT / markdown_name).read_text(encoding="utf-8")
        for alt, relative in re.findall(
            r"!\[([^\]]*)\]\((assets/diagrams/[^)]+\.svg)\)", text
        ):
            assert len(alt.strip()) >= 45, (markdown_name, relative, alt)
            assert alt.strip().lower() not in {"diagramma", "immagine", "schema"}


def test_visual_inventory_tracks_every_current_svg() -> None:
    inventory = (CONTENT_ROOT / "VISUALS.md").read_text(encoding="utf-8")
    for filename in EXPECTED_DIAGRAMS:
        assert filename in inventory
        assert re.search(
            rf"\|[^\n]*\|\s*integrato\s*\|\s*`assets/diagrams/{re.escape(filename)}`\s*\|",
            inventory,
        ), filename


def test_private_repository_defines_no_github_actions_workflow() -> None:
    workflow_root = ROOT / ".github" / "workflows"
    workflows = [] if not workflow_root.exists() else list(workflow_root.glob("*.y*ml"))
    assert workflows == []
