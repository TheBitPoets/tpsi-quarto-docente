from __future__ import annotations

import re
from pathlib import Path
import xml.etree.ElementTree as ET

import pytest


ROOT = Path(__file__).resolve().parents[1]
CONTENT_ROOT = ROOT / "content" / "tpsi_quarto"
DIAGRAM_ROOT = CONTENT_ROOT / "assets" / "diagrams"
VISUAL_GUIDE_ROOT = CONTENT_ROOT / "visuals"
SVG_NS = "http://www.w3.org/2000/svg"

EXPECTED_DIAGRAMS = {
    "01-execution-models.svg",
    "01-fork-exec-wait.svg",
    "01-lost-update.svg",
    "01-process-lifecycle.svg",
    "01-process-thread-resources.svg",
    "02-condition-wait.svg",
    "02-deadlock-cycle.svg",
    "02-monitor.svg",
    "02-pipe-parent-child.svg",
    "02-producer-consumer-buffer.svg",
    "02-race-read-modify-write.svg",
    "02-single-owner.svg",
    "03-requirement-concepts.svg",
    "03-requirements-traceability.svg",
    "04-architecture-layers.svg",
    "04-git-workflow.svg",
    "04-provenance.svg",
    "05-content-lifecycle.svg",
    "05-debug-cycle.svg",
    "05-quality-pipeline.svg",
    "05-test-levels.svg",
    "05-verification-validation.svg",
    "06-data-minimization.svg",
    "06-provenance-roles.svg",
    "06-responsible-ai.svg",
    "06-supply-chain.svg",
    "06-usage-rights.svg",
}

PRIMARY_REFERENCES = {
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

VISUAL_GUIDES = {
    "01_PROCESSI_E_CONCORRENZA.md": {name for name in EXPECTED_DIAGRAMS if name.startswith("01-")},
    "02_COMUNICAZIONE_E_SINCRONIZZAZIONE.md": {name for name in EXPECTED_DIAGRAMS if name.startswith("02-")},
    "03_REQUISITI_SOFTWARE.md": {name for name in EXPECTED_DIAGRAMS if name.startswith("03-")},
    "04_DOCUMENTAZIONE_VERSIONAMENTO.md": {name for name in EXPECTED_DIAGRAMS if name.startswith("04-")},
    "05_TESTING_DEBUGGING.md": {name for name in EXPECTED_DIAGRAMS if name.startswith("05-")},
    "06_CITTADINANZA_DIGITALE.md": {name for name in EXPECTED_DIAGRAMS if name.startswith("06-")},
}

IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+\.svg)\)")


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

    lowered = raw.lower()
    assert "<script" not in lowered
    assert "http://" not in raw.replace("http://www.w3.org/2000/svg", "")
    assert "https://" not in raw
    assert "@import" not in lowered
    assert "javascript:" not in lowered
    assert "font-family" in lowered or re.search(r"\bfont\s*:", lowered)


def test_expected_diagram_set_has_no_missing_or_accidental_extra_assets() -> None:
    actual = {path.name for path in DIAGRAM_ROOT.glob("*.svg")}
    assert actual == EXPECTED_DIAGRAMS
    assert len(actual) == 27


@pytest.mark.parametrize("markdown_name", sorted(PRIMARY_REFERENCES))
def test_primary_module_replacements_keep_text_fallback(markdown_name: str) -> None:
    markdown_path = CONTENT_ROOT / markdown_name
    text = markdown_path.read_text(encoding="utf-8")

    references = set(re.findall(r"\]\((assets/diagrams/[^)]+\.svg)\)", text))
    assert PRIMARY_REFERENCES[markdown_name] <= references

    for relative in PRIMARY_REFERENCES[markdown_name]:
        assert (CONTENT_ROOT / relative).is_file(), relative

    assert text.count("<details>") >= len(PRIMARY_REFERENCES[markdown_name])
    assert text.count("Versione testuale") >= len(PRIMARY_REFERENCES[markdown_name])


@pytest.mark.parametrize("guide_name", sorted(VISUAL_GUIDES))
def test_each_visual_guide_references_its_complete_module_set(guide_name: str) -> None:
    guide_path = VISUAL_GUIDE_ROOT / guide_name
    text = guide_path.read_text(encoding="utf-8")
    references = {Path(relative).name for _, relative in IMAGE_RE.findall(text)}

    assert references == VISUAL_GUIDES[guide_name]
    for filename in references:
        assert (DIAGRAM_ROOT / filename).is_file(), filename


@pytest.mark.parametrize(
    "markdown_path",
    sorted(
        list(PRIMARY_REFERENCES)
        + [f"visuals/{name}" for name in VISUAL_GUIDES]
    ),
)
def test_every_embedded_image_has_meaningful_alt_text(markdown_path: str) -> None:
    text = (CONTENT_ROOT / markdown_path).read_text(encoding="utf-8")
    images = IMAGE_RE.findall(text)
    assert images

    for alt, relative in images:
        assert len(alt.strip()) >= 45, (markdown_path, relative, alt)
        assert alt.strip().lower() not in {"diagramma", "immagine", "schema"}
        assert "../assets/diagrams/" in relative or "assets/diagrams/" in relative


def test_every_svg_is_referenced_by_a_visual_guide() -> None:
    referenced: set[str] = set()
    for guide_name in VISUAL_GUIDES:
        text = (VISUAL_GUIDE_ROOT / guide_name).read_text(encoding="utf-8")
        referenced.update(Path(relative).name for _, relative in IMAGE_RE.findall(text))
    assert referenced == EXPECTED_DIAGRAMS


def test_visual_inventory_tracks_every_current_svg_as_integrated() -> None:
    inventory = (CONTENT_ROOT / "VISUALS.md").read_text(encoding="utf-8")
    assert "SVG presenti: **27**" in inventory
    assert "diagrammi del libro copiati o ricalcati: **0**" in inventory

    for filename in EXPECTED_DIAGRAMS:
        assert filename in inventory
        assert re.search(
            rf"\|[^\n]*\|\s*integrato\s*\|\s*`assets/diagrams/{re.escape(filename)}`\s*\|",
            inventory,
        ), filename


def test_resource_index_links_all_visual_guides() -> None:
    index = (CONTENT_ROOT / "README.md").read_text(encoding="utf-8")
    for guide_name in VISUAL_GUIDES:
        assert f"visuals/{guide_name}" in index
    assert "27 diagrammi SVG originali" in index


def test_private_repository_defines_no_github_actions_workflow() -> None:
    workflow_root = ROOT / ".github" / "workflows"
    workflows = [] if not workflow_root.exists() else list(workflow_root.glob("*.y*ml"))
    assert workflows == []
