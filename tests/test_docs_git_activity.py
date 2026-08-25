from __future__ import annotations

import json
from pathlib import Path

from scripts.validate_activity import validate_activity


ROOT = Path(__file__).resolve().parents[1]
ACTIVITY_ROOT = ROOT / "activities" / "tpsi_quarto" / "docs_git_review"
ACTIVITY_PATH = ACTIVITY_ROOT / "activity.json"
PACK_PATH = ROOT / "content" / "tpsi_quarto" / "content-pack.json"
MANIFEST_PATH = ROOT / "content" / "tpsi_quarto" / "manifest.json"
ACTIVITY_ID = "tpsi4-activity-c-docs-git-review-001"
CONTENT_ID = "tpsi4-content-documentazione-versionamento"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_docs_git_activity_contract_registration_and_assets() -> None:
    activity = load_json(ACTIVITY_PATH)
    pack = load_json(PACK_PATH)
    manifest = load_json(MANIFEST_PATH)

    assert validate_activity(activity, str(ACTIVITY_PATH)) == []
    assert activity["id"] == ACTIVITY_ID
    assert activity["linguaggio"] == "markdown"
    assert activity["contesto"]["uda"] == "uda-14"
    assert activity["content_ids"] == [CONTENT_ID]
    assert activity["correzione"] == {
        "compila": False,
        "test": False,
        "sandbox": False,
        "ai_feedback": False,
    }
    assert sum(item["punti"] for item in activity["rubrica"]) == 10

    assert pack["version"] == manifest["version"] == "0.4.0"
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
        "PROJECT_README.md",
        "ADR-001.md",
        "PR_DESCRIPTION.md",
        "REVIEW.md",
        "EVIDENCE.md",
        "README.md",
    }


def test_templates_cover_docs_as_code_and_review_contract() -> None:
    project_readme = (ACTIVITY_ROOT / "starter" / "PROJECT_README.md").read_text(
        encoding="utf-8"
    )
    adr = (ACTIVITY_ROOT / "starter" / "ADR-001.md").read_text(encoding="utf-8")
    pr = (ACTIVITY_ROOT / "starter" / "PR_DESCRIPTION.md").read_text(
        encoding="utf-8"
    )
    review = (ACTIVITY_ROOT / "starter" / "REVIEW.md").read_text(encoding="utf-8")
    evidence = (ACTIVITY_ROOT / "starter" / "EVIDENCE.md").read_text(
        encoding="utf-8"
    )

    for heading in ("## Scopo", "## Avvio / prova minima", "## Limiti attuali", "## Provenienza e riferimenti"):
        assert heading in project_readme

    for heading in ("## Contesto", "## Decisione", "## Alternative considerate", "## Conseguenze negative / costi"):
        assert heading in adr

    for heading in ("## Problema", "## Requisiti collegati", "## Verifiche eseguite", "## Rischi e limiti"):
        assert heading in pr

    assert review.count("### R-") >= 3
    assert "blocking" in review
    assert "important" in review
    assert "suggestion" in review
    assert "style" in review

    for command in (
        "git branch --show-current",
        "git status -sb",
        "git log --oneline -n 5",
        "git diff --stat BASE...HEAD",
    ):
        assert command in evidence


def test_activity_keeps_git_history_as_manual_evidence_not_fake_autograding() -> None:
    activity = load_json(ACTIVITY_PATH)
    student_guide = (ACTIVITY_ROOT / "student" / "README.md").read_text(
        encoding="utf-8"
    )
    teacher_reference = (ACTIVITY_ROOT / "teacher" / "REFERENCE.md").read_text(
        encoding="utf-8"
    )

    assert activity["correzione"]["test"] is False
    assert len(activity["manual_checks"]) >= 5
    assert "almeno due commit" in student_guide.lower()
    assert "storia Git" in teacher_reference
    assert "RF/RNF -> file -> verifica" in teacher_reference
