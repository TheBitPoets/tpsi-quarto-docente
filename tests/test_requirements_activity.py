from __future__ import annotations

import csv
import io
import json
from pathlib import Path

from scripts.validate_activity import validate_activity


ROOT = Path(__file__).resolve().parents[1]
ACTIVITY_ROOT = ROOT / "activities" / "tpsi_quarto" / "mini_srs_traceability"
ACTIVITY_PATH = ACTIVITY_ROOT / "activity.json"
PACK_PATH = ROOT / "content" / "tpsi_quarto" / "content-pack.json"
MANIFEST_PATH = ROOT / "content" / "tpsi_quarto" / "manifest.json"
ACTIVITY_ID = "tpsi4-activity-c-mini-srs-traceability-001"
CONTENT_ID = "tpsi4-content-requisiti-software"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_requirements_activity_contract_registration_and_assets() -> None:
    activity = load_json(ACTIVITY_PATH)
    pack = load_json(PACK_PATH)
    manifest = load_json(MANIFEST_PATH)

    assert validate_activity(activity, str(ACTIVITY_PATH)) == []
    assert activity["id"] == ACTIVITY_ID
    assert activity["linguaggio"] == "markdown"
    assert activity["contesto"]["uda"] == "uda-13"
    assert activity["content_ids"] == [CONTENT_ID]
    assert activity["correzione"] == {
        "compila": False,
        "test": False,
        "sandbox": False,
        "ai_feedback": False,
    }
    assert sum(item["punti"] for item in activity["rubrica"]) == 10

    assert pack["version"] == manifest["version"] == "0.3.0"
    assert pack["status"] == manifest["status"] == "draft"

    pack_item = next(item for item in pack["content_items"] if item["id"] == CONTENT_ID)
    legacy_item = next(
        item for item in manifest["content_items"] if item["id"] == CONTENT_ID
    )
    assert pack_item["activity_ids"] == [ACTIVITY_ID]
    assert legacy_item["activity_ids"] == [ACTIVITY_ID]

    student_targets: set[str] = set()
    for asset in activity["assets"]:
        path = ACTIVITY_ROOT / asset["path"]
        assert path.is_file(), path
        if asset["visibility"] == "student":
            target = asset.get("target_path")
            assert target
            assert target not in student_targets
            student_targets.add(target)
            assert asset["type"] not in {"teacher_only", "hidden_test"}
        else:
            assert asset["visibility"] == "teacher"

    assert student_targets == {"SRS.md", "TRACEABILITY.csv", "README.md"}


def test_starter_encodes_the_minimum_traceability_contract() -> None:
    srs = (ACTIVITY_ROOT / "starter" / "SRS.md").read_text(encoding="utf-8")
    traceability = (ACTIVITY_ROOT / "starter" / "TRACEABILITY.csv").read_text(
        encoding="utf-8"
    )

    for requirement_id in (
        "RF-01",
        "RF-02",
        "RF-03",
        "RF-04",
        "RNF-01",
        "RNF-02",
        "RNF-03",
    ):
        assert requirement_id in srs

    assert "UC-01" in srs
    assert "Won't now" in srs
    assert "AC-07" in srs

    rows = list(csv.DictReader(io.StringIO(traceability)))
    assert [row["requirement_id"] for row in rows] == [
        "RF-01",
        "RF-02",
        "RF-03",
        "RF-04",
        "RNF-01",
        "RNF-02",
        "RNF-03",
    ]
    assert set(rows[0]) == {
        "requirement_id",
        "source_or_stakeholder",
        "acceptance_criterion",
        "evidence",
    }


def test_teacher_reference_demonstrates_requirement_to_evidence_chain() -> None:
    reference = (ACTIVITY_ROOT / "teacher" / "REFERENCE.md").read_text(
        encoding="utf-8"
    )

    for requirement_id in (
        "RF-01",
        "RF-02",
        "RF-03",
        "RF-04",
        "RNF-01",
        "RNF-02",
        "RNF-03",
    ):
        assert requirement_id in reference

    for criterion_id in ("AC-01", "AC-02", "AC-03", "AC-04", "AC-05", "AC-06", "AC-07"):
        assert criterion_id in reference

    assert "WN-01" in reference
    assert "WN-02" in reference
    assert "stakeholder -> requisito -> criterio -> evidenza" in reference


def test_activity_does_not_claim_deterministic_grading_for_subjective_srs() -> None:
    activity = load_json(ACTIVITY_PATH)
    student_guide = (ACTIVITY_ROOT / "student" / "README.md").read_text(
        encoding="utf-8"
    )

    assert activity["correzione"]["test"] is False
    assert activity["correzione"]["compila"] is False
    assert activity["correzione"]["sandbox"] is False
    assert "Non esiste una sola SRS corretta" in student_guide
    assert len(activity["manual_checks"]) >= 5
