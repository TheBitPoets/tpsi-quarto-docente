from __future__ import annotations

import json
from pathlib import Path

from scripts.validate_activity import validate_activity


ROOT = Path(__file__).resolve().parents[1]
ACTIVITY_ROOT = ROOT / "activities" / "tpsi_quarto" / "responsible_capstone"
ACTIVITY_PATH = ACTIVITY_ROOT / "activity.json"
PACK_PATH = ROOT / "content" / "tpsi_quarto" / "content-pack.json"
MANIFEST_PATH = ROOT / "content" / "tpsi_quarto" / "manifest.json"
COVERAGE_PATH = ROOT / "content" / "tpsi_quarto" / "COVERAGE.md"
ACTIVITY_ID = "tpsi4-activity-d-responsible-capstone-001"
CONTENT_ID = "tpsi4-content-cittadinanza-digitale"

EXPECTED_MODULE_ACTIVITIES = {
    "tpsi4-content-processi-concorrenza": [
        "tpsi4-activity-c-fork-pipe-square-001",
    ],
    "tpsi4-content-comunicazione-sincronizzazione": [
        "tpsi4-activity-c-fork-pipe-square-001",
        "tpsi4-activity-c-producer-consumer-buffer-001",
    ],
    "tpsi4-content-requisiti-software": [
        "tpsi4-activity-c-mini-srs-traceability-001",
    ],
    "tpsi4-content-documentazione-versionamento": [
        "tpsi4-activity-c-docs-git-review-001",
    ],
    "tpsi4-content-testing-debugging": [
        "tpsi4-activity-c-memory-debug-regression-001",
    ],
    "tpsi4-content-cittadinanza-digitale": [
        "tpsi4-activity-d-responsible-capstone-001",
    ],
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_capstone_contract_registration_and_assets() -> None:
    activity = load_json(ACTIVITY_PATH)
    pack = load_json(PACK_PATH)
    manifest = load_json(MANIFEST_PATH)

    assert validate_activity(activity, str(ACTIVITY_PATH)) == []
    assert activity["id"] == ACTIVITY_ID
    assert activity["difficolta"] == "D"
    assert activity["linguaggio"] == "markdown"
    assert activity["contesto"]["uda"] == "uda-16"
    assert activity["content_ids"] == [CONTENT_ID]
    assert activity["correzione"] == {
        "compila": False,
        "test": False,
        "sandbox": False,
        "ai_feedback": False,
    }
    assert sum(item["punti"] for item in activity["rubrica"]) == 10

    assert pack["version"] == manifest["version"] == "0.6.0"
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

    assert student_targets == {
        "FINAL_REPORT.md",
        "SOURCES.json",
        "PRIVACY_SECURITY.md",
        "ACCESSIBILITY_AI.md",
        "README.md",
    }


def test_every_tpsi4_module_has_at_least_one_canonical_activity() -> None:
    pack = load_json(PACK_PATH)
    manifest = load_json(MANIFEST_PATH)

    pack_mapping = {
        item["id"]: item["activity_ids"] for item in pack["content_items"]
    }
    legacy_mapping = {
        item["id"]: item["activity_ids"] for item in manifest["content_items"]
    }

    assert pack_mapping == EXPECTED_MODULE_ACTIVITIES
    assert legacy_mapping == EXPECTED_MODULE_ACTIVITIES
    assert all(pack_mapping.values())
    assert len(pack_mapping) == 6

    coverage = COVERAGE_PATH.read_text(encoding="utf-8")
    assert "## Copertura minima assegnabile per modulo" in coverage
    assert "6/6 moduli hanno almeno una Activity canonica" in coverage
    assert "non implica che ogni sua voce curricolare" in coverage


def test_sources_starter_is_valid_and_requires_provenance_fields() -> None:
    sources = load_json(ACTIVITY_ROOT / "starter" / "SOURCES.json")

    assert sources["schema_version"] == "1.0"
    assert isinstance(sources["sources"], list)
    assert len(sources["sources"]) >= 2

    required = {
        "source_id",
        "title",
        "provider",
        "uri_or_repository",
        "ref_or_version",
        "license_status",
        "use_in_project",
        "transformation",
        "redistribution_note",
    }
    for source in sources["sources"]:
        assert required <= set(source)
        assert source["source_id"]


def test_capstone_templates_keep_evidence_and_responsibility_boundaries_explicit() -> None:
    final_report = (ACTIVITY_ROOT / "starter" / "FINAL_REPORT.md").read_text(
        encoding="utf-8"
    )
    privacy = (ACTIVITY_ROOT / "starter" / "PRIVACY_SECURITY.md").read_text(
        encoding="utf-8"
    )
    accessibility_ai = (
        ACTIVITY_ROOT / "starter" / "ACCESSIBILITY_AI.md"
    ).read_text(encoding="utf-8")
    guide = (ACTIVITY_ROOT / "student" / "README.md").read_text(
        encoding="utf-8"
    )

    assert "## 6. Controlli NON eseguiti" in final_report
    assert "rischi residui" in final_report.lower()
    assert "## 1. Inventario dei dati" in privacy
    assert "## 5. Supply-chain" in privacy
    assert "## 2. Uso di AI" in accessibility_ai
    assert "AI non usata" in accessibility_ai
    assert "## 3. Limiti dell'automazione" in accessibility_ai
    assert "La CI è verde, quindi è sicuro" in guide
    assert "È online, quindi posso copiarlo" in guide


def test_capstone_is_manual_rubric_not_fake_autograding() -> None:
    activity = load_json(ACTIVITY_PATH)
    reference = (ACTIVITY_ROOT / "teacher" / "REFERENCE.md").read_text(
        encoding="utf-8"
    )

    assert activity["correzione"]["test"] is False
    assert activity["correzione"]["compila"] is False
    assert activity["correzione"]["sandbox"] is False
    assert len(activity["manual_checks"]) >= 5
    assert "Un progetto piccolo con limiti dichiarati" in reference
    assert "test/controlli realmente eseguiti" in reference
