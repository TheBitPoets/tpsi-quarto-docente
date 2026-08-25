from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

from scripts.validate_activity import validate_activity


ROOT = Path(__file__).resolve().parents[1]
ACTIVITY_ROOT = ROOT / "activities" / "tpsi_quarto" / "memory_debug_regression"
ACTIVITY_PATH = ACTIVITY_ROOT / "activity.json"
PACK_PATH = ROOT / "content" / "tpsi_quarto" / "content-pack.json"
MANIFEST_PATH = ROOT / "content" / "tpsi_quarto" / "manifest.json"
ACTIVITY_ID = "tpsi4-activity-c-memory-debug-regression-001"
CONTENT_ID = "tpsi4-content-testing-debugging"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_output(value: str) -> str:
    return value.replace("\r\n", "\n").strip()


def compile_c(source: Path, output: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["gcc", "-Wall", "-Wextra", "-Wpedantic", "-std=c17", str(source), "-o", str(output)],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )


def test_debug_activity_contract_registration_and_assets() -> None:
    activity = load_json(ACTIVITY_PATH)
    pack = load_json(PACK_PATH)
    manifest = load_json(MANIFEST_PATH)

    assert validate_activity(activity, str(ACTIVITY_PATH)) == []
    assert activity["id"] == ACTIVITY_ID
    assert activity["tipo"] == "debug-didattico"
    assert activity["contesto"]["uda"] == "uda-15"
    assert activity["content_ids"] == [CONTENT_ID]
    assert sum(item["punti"] for item in activity["rubrica"]) == 10

    assert pack["version"] == manifest["version"] == "0.5.0"
    assert pack["status"] == manifest["status"] == "draft"
    pack_item = next(item for item in pack["content_items"] if item["id"] == CONTENT_ID)
    legacy_item = next(item for item in manifest["content_items"] if item["id"] == CONTENT_ID)
    assert pack_item["activity_ids"] == [ACTIVITY_ID]
    assert legacy_item["activity_ids"] == [ACTIVITY_ID]

    targets = set()
    for asset in activity["assets"]:
        assert (ACTIVITY_ROOT / asset["path"]).is_file()
        if asset["visibility"] == "student":
            target = asset.get("target_path")
            assert target and target not in targets
            targets.add(target)
        else:
            assert asset["visibility"] == "teacher"
    assert targets == {"main.c", "REGRESSION.md", "README.md"}


@pytest.mark.skipif(
    not sys.platform.startswith("linux") or shutil.which("gcc") is None,
    reason="La verifica C richiede Linux con gcc.",
)
def test_reference_solution_compiles_and_passes_declared_cases(tmp_path: Path) -> None:
    activity = load_json(ACTIVITY_PATH)
    binary = tmp_path / "debug_solution"
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
        assert result.returncode == 0
        assert normalize_output(result.stdout) == normalize_output(case["expected_stdout"])

    invalid = subprocess.run(
        [str(binary)], input="abc\n", capture_output=True, text=True, timeout=5, check=False
    )
    assert invalid.returncode != 0
    assert normalize_output(invalid.stdout) == "Input non valido"


@pytest.mark.skipif(
    not sys.platform.startswith("linux") or shutil.which("gcc") is None,
    reason="La verifica C richiede Linux con gcc.",
)
def test_starter_compiles_but_exposes_the_functional_regression(tmp_path: Path) -> None:
    binary = tmp_path / "debug_starter"
    compilation = compile_c(ACTIVITY_ROOT / "starter" / "main.c", binary)
    assert compilation.returncode == 0, compilation.stderr
    assert compilation.stderr == ""

    result = subprocess.run(
        [str(binary)], input="5\n", capture_output=True, text=True, timeout=5, check=False
    )
    assert result.returncode == 0
    assert normalize_output(result.stdout) != "Somma: 15\nMin: 1\nMax: 5"


def test_regression_template_requires_root_cause_and_sanitizer_evidence() -> None:
    report = (ACTIVITY_ROOT / "starter" / "REGRESSION.md").read_text(encoding="utf-8")
    guide = (ACTIVITY_ROOT / "student" / "README.md").read_text(encoding="utf-8")
    assert "## Causa radice" in report
    assert "## Test di regressione" in report
    assert "-fsanitize=address,undefined" in report
    assert "ipotesi" in guide.lower()
    assert "ASan" in guide
