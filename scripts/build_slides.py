#!/usr/bin/env python3
"""Validate and build TPSI4 Marp decks into HTML, PDF and PPTX artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
SLIDES_ROOT = ROOT / "slides" / "tpsi4"
MODULES_ROOT = SLIDES_ROOT / "modules"
CONTENT_ROOT = ROOT / "content" / "tpsi_quarto"
ROOT_README = ROOT / "README.md"
SLIDES_README = SLIDES_ROOT / "README.md"
MARP_CLI_VERSION = "4.5.0"
MARP_PACKAGE = f"@marp-team/marp-cli@{MARP_CLI_VERSION}"
MODULE_RE = re.compile(r"^(\d{2})_[A-Z0-9_]+\.md$")
EXPECTED_MODULES = tuple(f"{i:02d}" for i in range(7))


def discover_decks() -> list[Path]:
    return sorted(p for p in MODULES_ROOT.glob("*.md") if MODULE_RE.match(p.name))


def _front_matter(text: str) -> str:
    if not text.startswith("---\n"):
        return ""
    end = text.find("\n---\n", 4)
    return "" if end < 0 else text[4:end]


def canonical_for(deck: Path) -> Path:
    number = deck.name[:2]
    if number == "00":
        return CONTENT_ROOT / "README.md"
    matches = sorted(CONTENT_ROOT.glob(f"{number}_*.md"))
    if len(matches) != 1:
        raise SystemExit(f"expected exactly one canonical module for {number}, found {len(matches)}")
    return matches[0]


def validate_sources() -> None:
    errors: list[str] = []
    decks = discover_decks()
    numbers = tuple(p.name[:2] for p in decks)
    if numbers != EXPECTED_MODULES:
        errors.append(f"expected slide decks 00..06, found: {numbers}")

    slide_index = SLIDES_README.read_text(encoding="utf-8") if SLIDES_README.exists() else ""
    root_index = ROOT_README.read_text(encoding="utf-8") if ROOT_README.exists() else ""

    for deck in decks:
        canonical = canonical_for(deck)
        if not canonical.exists():
            errors.append(f"{deck}: missing canonical lesson {canonical}")
        if deck.name[:2] != "00" and deck.stem != canonical.stem:
            errors.append(f"{deck}: stem differs from canonical content {canonical.name}")

        text = deck.read_text(encoding="utf-8")
        fm = _front_matter(text)
        if not fm or not re.search(r"(?m)^marp:\s*true\s*$", fm):
            errors.append(f"{deck}: missing Marp front matter")
        if "obiettivi" not in text.lower():
            errors.append(f"{deck}: missing objectives")
        if "checkpoint" not in text.lower():
            errors.append(f"{deck}: missing checkpoint")

        slide_link = f"modules/{deck.name}"
        if slide_link not in slide_index:
            errors.append(f"slides/tpsi4/README.md: missing link to {slide_link}")
        root_link = f"slides/tpsi4/{slide_link}"
        if root_link not in root_index:
            errors.append(f"README.md: missing link to {root_link}")

    for required in ("teacher/README.md", "student/README.md", "doc/DELIVERY_CHANGELOG.md"):
        if required not in root_index:
            errors.append(f"README.md: missing delivery entry point {required}")

    if errors:
        raise SystemExit("TPSI4 slide delivery validation failed:\n- " + "\n- ".join(errors))


def _generated_path(source: Path, fmt: str) -> Path:
    return source.with_suffix(f".{fmt}")


def _run_marp(inputs: Iterable[Path], output_dir: Path, fmt: str, browser: str) -> None:
    npx = shutil.which("npx")
    if not npx:
        raise SystemExit("npx not found: install Node.js 18+ before building slides")

    decks = list(inputs)
    output_dir.mkdir(parents=True, exist_ok=True)
    generated = [_generated_path(source, fmt) for source in decks]
    for path in generated:
        path.unlink(missing_ok=True)

    parallelism = "1" if fmt == "pptx" else "4"
    cmd = [npx, "--yes", MARP_PACKAGE, "--html", "--allow-local-files", "--parallel", parallelism]
    if fmt == "pdf":
        cmd.extend(["--pdf", "--pdf-outlines", "--browser", browser])
    elif fmt == "pptx":
        cmd.extend(["--pptx", "--browser", browser])
    elif fmt != "html":
        raise ValueError(f"unsupported format: {fmt}")
    cmd.extend(str(p.relative_to(ROOT)) for p in decks)

    try:
        subprocess.run(cmd, cwd=ROOT, check=True)
        for source, built in zip(decks, generated):
            if not built.exists():
                raise SystemExit(f"Marp did not produce expected artifact: {built}")
            relative = source.relative_to(SLIDES_ROOT).with_suffix(f".{fmt}")
            destination = output_dir / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(built), str(destination))
    finally:
        for path in generated:
            path.unlink(missing_ok=True)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_manifest(output_root: Path, formats: list[str]) -> None:
    artifacts = []
    for path in sorted(output_root.rglob("*")):
        if path.is_file() and path.name not in {"MANIFEST.json", "SHA256SUMS.txt"}:
            artifacts.append({
                "path": path.relative_to(output_root).as_posix(),
                "sha256": _sha256(path),
                "bytes": path.stat().st_size,
            })
    sources = [
        {"path": p.relative_to(ROOT).as_posix(), "sha256": _sha256(p)}
        for p in discover_decks()
    ]
    manifest = {
        "schema": "thebitpoets.course-slides-artifact.v1",
        "course": "tpsi-quarto-2026-2027",
        "content_pack": "0.1.0",
        "content_pack_status": "draft",
        "marp_cli": MARP_CLI_VERSION,
        "commit": os.environ.get("SOURCE_SHA") or os.environ.get("GITHUB_SHA"),
        "formats": formats,
        "source_decks": sources,
        "artifacts": artifacts,
    }
    (output_root / "MANIFEST.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (output_root / "SHA256SUMS.txt").write_text(
        "".join(f"{item['sha256']}  {item['path']}\n" for item in artifacts), encoding="utf-8"
    )


def build(output_root: Path, formats: list[str], browser: str) -> None:
    validate_sources()
    if output_root.exists():
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True)
    decks = discover_decks()
    for fmt in formats:
        _run_marp(decks, output_root / fmt, fmt, browser)
    write_manifest(output_root, formats)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "build" / "tpsi4-slides")
    parser.add_argument("--formats", default="html,pdf,pptx")
    parser.add_argument("--browser", default="chrome")
    parser.add_argument("--check-only", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    formats = [part.strip() for part in args.formats.split(",") if part.strip()]
    invalid = sorted(set(formats) - {"html", "pdf", "pptx"})
    if invalid:
        raise SystemExit(f"unsupported formats: {', '.join(invalid)}")
    validate_sources()
    if args.check_only:
        print(f"OK: 7 TPSI4 decks; Marp CLI pinned at {MARP_CLI_VERSION}")
        return 0
    output = args.output if args.output.is_absolute() else ROOT / args.output
    build(output, formats, args.browser)
    print(f"Built {len(discover_decks())} decks in {', '.join(formats)} -> {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
