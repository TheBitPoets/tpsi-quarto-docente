from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

from scripts.validate_activity import validate_activity


ROOT = Path(__file__).resolve().parents[1]
ACTIVITY_ROOT = ROOT / "activities" / "tpsi_quarto" / "producer_consumer_buffer"
ACTIVITY_PATH = ACTIVITY_ROOT / "activity.json"
PACK_PATH = ROOT / "content" / "tpsi_quarto" / "content-pack.json"
MANIFEST_PATH = ROOT / "content" / "tpsi_quarto" / "manifest.json"
ACTIVITY_ID = "tpsi4-activity-c-producer-consumer-buffer-001"
CONTENT_ID = "tpsi4-content-comunicazione-sincronizzazione"


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
            "-pthread",
            str(source),
            "-o",
            str(output),
        ],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )


def test_activity_contract_and_registration() -> None:
    activity = load_json(ACTIVITY_PATH)
    pack = load_json(PACK_PATH)
    manifest = load_json(MANIFEST_PATH)

    assert validate_activity(activity, str(ACTIVITY_PATH)) == []
    assert activity["id"] == ACTIVITY_ID
    assert activity["linguaggio"] == "c"
    assert activity["contesto"]["uda"] == "uda-12"
    assert activity["content_ids"] == [CONTENT_ID]
    assert sum(item["punti"] for item in activity["rubrica"]) == 10

    assert pack["version"] == "0.2.0"
    assert manifest["version"] == "0.2.0"
    assert pack["status"] == manifest["status"] == "draft"

    pack_item = next(item for item in pack["content_items"] if item["id"] == CONTENT_ID)
    legacy_item = next(
        item for item in manifest["content_items"] if item["id"] == CONTENT_ID
    )
    assert ACTIVITY_ID in pack_item["activity_ids"]
    assert pack_item["activity_ids"] == legacy_item["activity_ids"]

    student_targets = set()
    for asset in activity["assets"]:
        asset_path = ACTIVITY_ROOT / asset["path"]
        assert asset_path.is_file(), asset_path
        if asset["visibility"] == "student":
            target = asset.get("target_path")
            assert target
            assert target not in student_targets
            student_targets.add(target)
            assert asset["type"] not in {"teacher_only", "hidden_test"}
        else:
            assert asset["visibility"] == "teacher"

    assert student_targets == {"main.c", "README.md"}


@pytest.mark.skipif(
    not sys.platform.startswith("linux") or shutil.which("gcc") is None,
    reason="Il laboratorio pthread richiede Linux con gcc.",
)
def test_reference_solution_compiles_and_passes_declared_cases(tmp_path: Path) -> None:
    activity = load_json(ACTIVITY_PATH)
    binary = tmp_path / "producer_consumer"
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
    reason="Il laboratorio pthread richiede Linux con gcc.",
)
def test_starter_compiles_but_does_not_solve_the_activity(tmp_path: Path) -> None:
    binary = tmp_path / "producer_consumer_starter"
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
    assert normalize_output(result.stdout) != "Somma: 15\nProdotti: 5\nConsumati: 5"
