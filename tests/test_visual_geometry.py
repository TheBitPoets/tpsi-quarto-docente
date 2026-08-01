from __future__ import annotations

import re
from pathlib import Path
import xml.etree.ElementTree as ET

import pytest


ROOT = Path(__file__).resolve().parents[1]
DIAGRAM_ROOT = ROOT / "content" / "tpsi_quarto" / "assets" / "diagrams"
SVG_NS = "http://www.w3.org/2000/svg"

CONNECTOR_CLEARANCE_CASES = [
    ("01-lost-update.svg", "write-a", "result-box"),
    ("01-lost-update.svg", "write-b", "result-box"),
    ("01-process-lifecycle.svg", "event-completed", "idea-key-box"),
]

# Widths were measured locally with DejaVu Sans/Mono at the SVG font size.
# The exact text is asserted as well, so a wording or font-size change requires
# an intentional remeasurement instead of silently weakening the regression.
TEXT_CONTAINMENT_CASES = [
    (
        "01-process-lifecycle.svg",
        "idea-key-text",
        "idea-key-box",
        [
            "“Pronto” non significa “in esecuzione”;",
            "“in attesa” non consuma CPU in polling continuo.",
        ],
        [348.6, 444.1],
    ),
    (
        "02-producer-consumer-buffer.svg",
        "mutex-text",
        "mutex-badge",
        ["mutex protegge indici e contatore"],
        [290.1],
    ),
    (
        "02-producer-consumer-buffer.svg",
        "full-card-text",
        "full-card",
        [
            "Il produttore attende la condizione",
            "not_full.",
            "Non sovrascrive elementi ancora da consumare.",
        ],
        [311.6, 97.6, 412.1],
    ),
    (
        "02-producer-consumer-buffer.svg",
        "empty-card-text",
        "empty-card",
        [
            "Il consumatore attende la condizione",
            "not_empty.",
            "Non estrae un elemento inesistente.",
        ],
        [333.9, 108.4, 310.3],
    ),
]


def _svg_root(filename: str) -> ET.Element:
    return ET.parse(DIAGRAM_ROOT / filename).getroot()


def _element_by_id(root: ET.Element, element_id: str) -> ET.Element:
    element = root.find(f".//*[@id='{element_id}']")
    assert element is not None, element_id
    return element


def _rect_bounds(rect: ET.Element) -> tuple[float, float, float, float]:
    left = float(rect.get("x", "0"))
    top = float(rect.get("y", "0"))
    return (
        left,
        top,
        left + float(rect.get("width", "0")),
        top + float(rect.get("height", "0")),
    )


def _sample_supported_path(path_data: str, samples: int = 400) -> list[tuple[float, float]]:
    horizontal = re.fullmatch(
        r"M\s*(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)\s+H\s*(-?\d+(?:\.\d+)?)",
        path_data.strip(),
    )
    if horizontal:
        x0, y0, x1 = map(float, horizontal.groups())
        return [(x0 + (x1 - x0) * index / samples, y0) for index in range(samples + 1)]

    cubic = re.fullmatch(
        r"M\s*(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)\s+"
        r"C\s*(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)\s+"
        r"(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)\s+"
        r"(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)",
        path_data.strip(),
    )
    if cubic:
        values = list(map(float, cubic.groups()))
        p0 = values[0:2]
        p1 = values[2:4]
        p2 = values[4:6]
        p3 = values[6:8]
        points: list[tuple[float, float]] = []
        for index in range(samples + 1):
            t = index / samples
            one_minus_t = 1.0 - t
            x = (
                one_minus_t**3 * p0[0]
                + 3 * one_minus_t**2 * t * p1[0]
                + 3 * one_minus_t * t**2 * p2[0]
                + t**3 * p3[0]
            )
            y = (
                one_minus_t**3 * p0[1]
                + 3 * one_minus_t**2 * t * p1[1]
                + 3 * one_minus_t * t**2 * p2[1]
                + t**3 * p3[1]
            )
            points.append((x, y))
        return points

    raise AssertionError(f"Formato path non supportato dal test: {path_data}")


def _text_lines_and_baselines(text: ET.Element) -> tuple[list[str], list[float], list[float]]:
    tspans = text.findall(f"{{{SVG_NS}}}tspan")
    base_y = float(text.get("y", "0"))
    inherited_font_size = float(text.get("font-size", "16"))

    if not tspans:
        return ["".join(text.itertext()).strip()], [base_y], [inherited_font_size]

    lines: list[str] = []
    baselines: list[float] = []
    font_sizes: list[float] = []
    current_y = base_y
    for tspan in tspans:
        current_y += float(tspan.get("dy", "0"))
        lines.append("".join(tspan.itertext()).strip())
        baselines.append(current_y)
        font_sizes.append(float(tspan.get("font-size", inherited_font_size)))
    return lines, baselines, font_sizes


@pytest.mark.parametrize("filename,path_id,node_id", CONNECTOR_CLEARANCE_CASES)
def test_reviewed_connectors_do_not_enter_nodes(
    filename: str, path_id: str, node_id: str
) -> None:
    root = _svg_root(filename)
    path = _element_by_id(root, path_id)
    node = _element_by_id(root, node_id)
    left, top, right, bottom = _rect_bounds(node)

    points = _sample_supported_path(path.get("d", ""))
    intersections = [
        (x, y)
        for x, y in points
        if left + 0.5 < x < right - 0.5 and top + 0.5 < y < bottom - 0.5
    ]
    assert intersections == [], (filename, path_id, node_id, intersections[:5])


@pytest.mark.parametrize(
    "filename,text_id,box_id,expected_lines,measured_widths",
    TEXT_CONTAINMENT_CASES,
)
def test_reviewed_text_stays_inside_its_box(
    filename: str,
    text_id: str,
    box_id: str,
    expected_lines: list[str],
    measured_widths: list[float],
) -> None:
    root = _svg_root(filename)
    text = _element_by_id(root, text_id)
    box = _element_by_id(root, box_id)
    assert text.get("data-contained-by") == box_id

    lines, baselines, font_sizes = _text_lines_and_baselines(text)
    assert lines == expected_lines
    assert len(lines) == len(measured_widths) == len(baselines) == len(font_sizes)

    left, top, right, bottom = _rect_bounds(box)
    usable_width = right - left - 40.0
    assert max(measured_widths) <= usable_width, (
        filename,
        text_id,
        max(measured_widths),
        usable_width,
    )

    for baseline, font_size in zip(baselines, font_sizes):
        assert baseline - font_size >= top + 10.0, (filename, text_id, baseline, top)
        assert baseline + font_size * 0.3 <= bottom - 10.0, (
            filename,
            text_id,
            baseline,
            bottom,
        )
