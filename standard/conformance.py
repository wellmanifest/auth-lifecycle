#!/usr/bin/env python3
"""Dependency-free stub conformance for auth-lifecycle v0.1.0-dev."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PACK = ROOT.parent
CLOSED_PROFILES = ("otp-email", "access-api", "session-continue")
REQUIRED_DOCS = (
    PACK / "README.md",
    PACK / "AGENTS.md",
    PACK / "docs/ARCHITECTURE.md",
    PACK / "VERSION",
)


class ContractError(ValueError):
    pass


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run() -> dict:
    for path in REQUIRED_DOCS:
        if not path.is_file():
            raise ContractError(f"missing required document: {path.relative_to(PACK)}")
    readme = (PACK / "README.md").read_text(encoding="utf-8")
    for profile in CLOSED_PROFILES:
        if f"`{profile}`" not in readme:
            raise ContractError(f"closed profile {profile} missing from README")
    version = (PACK / "VERSION").read_text(encoding="utf-8").strip()
    if version != "0.1.0-dev":
        raise ContractError("VERSION must be 0.1.0-dev for the skeleton")
    return {
        "schema": "wellmanifest.auth-lifecycle-conformance/v1",
        "ok": True,
        "profiles": list(CLOSED_PROFILES),
        "digests": {
            str(path.relative_to(PACK)): "sha256:" + file_digest(path)
            for path in REQUIRED_DOCS
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true")
    parser.parse_args()
    try:
        print(json.dumps(run(), ensure_ascii=False, indent=2, sort_keys=True))
    except ContractError as error:
        print(json.dumps({"ok": False, "error": str(error)}, ensure_ascii=False))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
