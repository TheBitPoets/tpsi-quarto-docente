from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

from scripts import course_source_catalog
from scripts.content_pack_contract import (
    project_course_design_sources,
    validate_content_pack,
)
from scripts.validate_activity import validate_activity


ROOT = Path(__file__).resolve().parents[1]
PACK_ROOT = ROOT / "content" / "tpsi_quarto"
MANIFEST_PATH = PACK_ROOT / "manifest.json"
CONTENT_PACK_V1_PATH = PACK_ROOT / "content-pack.json"
DESIGN_PATH = ROOT / "doc" / "course_designs" / "tpsi_quarto_2026_2027.json"
ACTIVITY_ROOT = ROOT / "activities" / "tpsi_quarto" / "fork_pipe_square"
ACTIVITY_PATH = ACTIVITY_ROOT / "activity.json"
LINUX_SOURCE_ID = "tpsi4-source-linux-programming"
PINNED_PLATFORM_SHA = "39936004d3dc777b4e56d089dac0e61a138a1913"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_output(value: str) -> str:
    return value.replace("\r\n", "\n").strip()


def compile_c(source: Path, output: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            "gcc",
            "-Wall",
            "-Wextra",
            "-Wpedantic",
            "-std=c17",
            str(source),
            "-o",
            str(output),
        ],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )


def test_legacy_v0_manifest_keeps_original_identity_and_declared_overlay() -> None:
    manifest = load_json(MANIFEST_PATH)

    assert manifest["schema_version"] == "thebitlab.content-pack.v0"
    assert manifest["status"] == "draft"
    assert manifest["policies"]["book_text_reproduction_forbidden"] is True
    assert manifest["policies"]["provenance_required"] is True
    assert manifest["policies"]["java_automatic_grading_enabled"] is False

    content_ids = set()
    for item in manifest["content_items"]:
        assert item["id"] not in content_ids
        content_ids.add(item["id"])
        assert (ROOT / item["path"]).is_file()

    sources = {source["id"]: source for source in manifest["sources"]}
    assert set(sources) == {
        "tpsi4-source-originali",
        LINUX_SOURCE_ID,
    }

    original = sources["tpsi4-source-originali"]
    for filename in original["files"]:
        assert (ROOT / original["path"] / filename).is_file()

    # Il v0 descriveva implicitamente un overlay col checkout di 2cornot2c.
    # Non inventiamo il file nel repo privato: la v1 rende questa dipendenza remota.
    legacy_linux = sources[LINUX_SOURCE_ID]
    assert legacy_linux.get("path", "") == ""
    assert legacy_linux["files"] == ["LINUX_PROGRAMMING.md"]
    assert not (ROOT / "LINUX_PROGRAMMING.md").exists()

    assert "tpsi4-content-processi-concorrenza" in content_ids
    assert "tpsi4-content-comunicazione-sincronizzazione" in content_ids


def test_content_pack_v1_is_valid_and_preserves_v0_identity() -> None:
    legacy = load_json(MANIFEST_PATH)
    pack = load_json(CONTENT_PACK_V1_PATH)

    assert validate_content_pack(
        pack,
        str(CONTENT_PACK_V1_PATH),
        root=ROOT,
    ) == []

    for field in ("id", "title", "version", "status", "language", "audience", "ownership"):
        assert pack[field] == legacy[field]

    assert [item["id"] for item in pack["references"]] == [
        item["id"] for item in legacy["curriculum_references"]
    ]
    assert [item["id"] for item in pack["content_items"]] == [
        item["id"] for item in legacy["content_items"]
    ]
    assert pack["course_designs"] == legacy["course_designs"]
    assert pack["activity_roots"] == legacy["activity_roots"]
    assert pack["coverage"] == {
        "path": "content/tpsi_quarto/COVERAGE.md",
        "status": "draft",
    }
    assert pack["policies"]["book_text_reproduction_forbidden"] is True
    assert pack["policies"]["restricted_source_copying_forbidden"] is True
    assert pack["extensions"]["v0_compatibility"] == legacy["compatibility"]

    for item in pack["content_items"]:
        assert item["source_refs"] == [
            {
                "id": "tpsi4-source-originali",
                "role": "content-origin",
                "locator": item["path"],
            }
        ]

    source_map = {source["id"]: source for source in pack["sources"]}
    linux = source_map[LINUX_SOURCE_ID]
    assert linux["provider"] == "github"
    assert linux["repository"] == "TheBitPoets/2cornot2c"
    assert linux["ref"] == PINNED_PLATFORM_SHA
    assert linux["files"] == ["LINUX_PROGRAMMING.md"]
    assert "path" not in linux


def test_content_pack_v1_sources_project_to_course_board_catalog() -> None:
    pack = load_json(CONTENT_PACK_V1_PATH)
    projected = project_course_design_sources(pack)
    normalized = course_source_catalog.normalize_course_sources(
        {"sources": projected}
    )

    assert [source.source_id for source in normalized] == [
        "tpsi4-source-originali",
        LINUX_SOURCE_ID,
    ]
    assert normalized[0].provider == "local"
    assert normalized[0].files == (
        "README.md",
        "COVERAGE.md",
        "01_PROCESSI_E_CONCORRENZA.md",
        "02_COMUNICAZIONE_E_SINCRONIZZAZIONE.md",
        "03_REQUISITI_SOFTWARE.md",
        "04_DOCUMENTAZIONE_VERSIONAMENTO.md",
        "05_TESTING_DEBUGGING.md",
        "06_CITTADINANZA_DIGITALE.md",
    )
    assert normalized[1].provider == "github"
    assert normalized[1].repository == "TheBitPoets/2cornot2c"
    assert normalized[1].ref == PINNED_PLATFORM_SHA
    assert normalized[1].files == ("LINUX_PROGRAMMING.md",)


def test_archived_course_design_remains_a_valid_33_week_legacy_design() -> None:
    design = load_json(DESIGN_PATH)
    source_files = course_source_catalog.local_markdown_source_files(design, ROOT)

    # Il CourseDesign storico mantiene ancora la vecchia sorgente overlay Linux.
    # In un checkout standalone vengono indicizzati soltanto gli otto file locali reali.
    indexed_paths = {item.relative_path for item in source_files}
    assert "LINUX_PROGRAMMING.md" not in indexed_paths
    assert "content/tpsi_quarto/01_PROCESSI_E_CONCORRENZA.md" in indexed_paths
    assert len(indexed_paths) == 8

    normalized_sources = course_source_catalog.normalize_course_sources(design)
    assert [source.source_id for source in normalized_sources] == [
        "tpsi4-source-originali",
        LINUX_SOURCE_ID,
    ]
    assert normalized_sources[1].provider == "local"
    assert normalized_sources[1].files == ("LINUX_PROGRAMMING.md",)

    years = design["years"]
    assert len(years) == 1
    year = years[0]
    assert year["id"] == "quarto-anno"
    assert year["weeks"] == 33
    assert sum(int(uda["weeks"]) for uda in year["udas"]) == 33
    assert [uda["id"] for uda in year["udas"]] == [
        "uda-10",
        "uda-11",
        "uda-12",
        "uda-13",
        "uda-14",
        "uda-15",
        "uda-16",
    ]

    for uda in year["udas"]:
        for item in uda.get("items", []):
            assert "controllo-dei-processi" not in item["id"]
            assert item.get("source_id") == "tpsi4-source-originali"
            assert (ROOT / item["source"]).is_file()


def test_activity_contract_assets_and_provenance() -> None:
    activity = load_json(ACTIVITY_PATH)
    legacy = load_json(MANIFEST_PATH)
    pack = load_json(CONTENT_PACK_V1_PATH)

    assert validate_activity(activity, str(ACTIVITY_PATH)) == []
    assert activity["id"] == "tpsi4-activity-c-fork-pipe-square-001"
    assert activity["linguaggio"] == "c"
    assert activity["student_support_mode"] == "feedback-tecnico"

    known_content_ids = {item["id"] for item in legacy["content_items"]}
    assert set(activity["content_ids"]) <= known_content_ids

    v1_sources = {source["id"]: source for source in pack["sources"]}
    for source_ref in activity["source_refs"]:
        source_id = source_ref["source_id"]
        assert source_id in v1_sources
        assert source_ref["anchor"]
        if source_id == "tpsi4-source-originali":
            assert (ROOT / source_ref["path"]).is_file()
        else:
            assert source_id == LINUX_SOURCE_ID
            assert source_ref["path"] == "LINUX_PROGRAMMING.md"
            assert v1_sources[source_id]["provider"] == "github"
            assert v1_sources[source_id]["ref"] == PINNED_PLATFORM_SHA

    student_targets = set()
    for asset in activity["assets"]:
        asset_path = ACTIVITY_ROOT / asset["path"]
        assert asset_path.is_file(), asset_path
        if asset["visibility"] == "student":
            assert asset["type"] not in {"hidden_test", "teacher_only"}
            target = asset.get("target_path")
            assert target
            assert target not in student_targets
            student_targets.add(target)
        else:
            assert asset["visibility"] == "teacher"

    assert student_targets == {"main.c", "README.md"}
    assert sum(item["punti"] for item in activity["rubrica"]) == 10


@pytest.mark.skipif(
    not sys.platform.startswith("linux") or shutil.which("gcc") is None,
    reason="Il laboratorio usa fork/pipe e richiede Linux con gcc.",
)
def test_verified_solution_compiles_and_passes_declared_cases(tmp_path: Path) -> None:
    activity = load_json(ACTIVITY_PATH)
    binary = tmp_path / "fork_pipe_square"
    compilation = compile_c(ACTIVITY_ROOT / "solution" / "main.c", binary)

    assert compilation.returncode == 0, compilation.stderr
    assert compilation.stderr == ""

    for case in activity["test_cases"]:
        result = subprocess.run(
            [str(binary)],
            input=case["stdin"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        assert result.returncode == 0, (case["name"], result.stderr)
        assert normalize_output(result.stdout) == normalize_output(
            case["expected_stdout"]
        ), case["name"]

    invalid = subprocess.run(
        [str(binary)],
        input="abc\n",
        capture_output=True,
        text=True,
        timeout=5,
        check=False,
    )
    assert invalid.returncode != 0
    assert normalize_output(invalid.stdout) == "Input non valido"


@pytest.mark.skipif(
    not sys.platform.startswith("linux") or shutil.which("gcc") is None,
    reason="Il laboratorio usa fork/pipe e richiede Linux con gcc.",
)
def test_starter_compiles_but_does_not_already_solve_the_lab(tmp_path: Path) -> None:
    binary = tmp_path / "fork_pipe_square_starter"
    compilation = compile_c(ACTIVITY_ROOT / "starter" / "main.c", binary)

    assert compilation.returncode == 0, compilation.stderr
    assert compilation.stderr == ""

    result = subprocess.run(
        [str(binary)],
        input="5\n",
        capture_output=True,
        text=True,
        timeout=5,
        check=False,
    )
    assert result.returncode == 0
    assert normalize_output(result.stdout) != "Risultato: 25"


def test_book_is_coverage_reference_not_imported_text() -> None:
    manifest = load_json(MANIFEST_PATH)
    references = manifest["curriculum_references"]

    assert len(references) == 1
    reference = references[0]
    assert reference["role"] == "coverage-reference"
    assert reference["license_status"] == "reference-only"
    assert reference["text_imported"] is False

    coverage = (PACK_ROOT / "COVERAGE.md").read_text(encoding="utf-8")
    assert "Processi sequenziali e paralleli" in coverage
    assert "Comunicazione e sincronizzazione" in coverage
    assert "Requisiti software" in coverage
    assert "Documentazione del software" in coverage
    assert "Testing e debugging" in coverage
    assert "Cittadinanza digitale" in coverage
