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
    PACK / "docs/SPEC.md",
    PACK / "VERSION",
    PACK / "schemas/auth-lifecycle.schema.json",
    PACK / "schemas/auth-lifecycle.v1.gbnf",
)
VALID_FIXTURE = ROOT / "fixtures/valid/otp-email-profile.json"
INVALID_FIXTURE = ROOT / "fixtures/invalid/unknown-profile.json"


class ContractError(ValueError):
    pass


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ContractError(f"invalid JSON in {path.relative_to(PACK)}: {error}") from error
    if not isinstance(data, dict):
        raise ContractError(f"expected object in {path.relative_to(PACK)}")
    return data


def check_profile_document(doc: dict, *, expect_valid: bool) -> None:
    profile_id = doc.get("profileId")
    known = profile_id in CLOSED_PROFILES
    if expect_valid and not known:
        raise ContractError(f"AUTHN-PROFILE-001: unknown profile {profile_id!r}")
    if not expect_valid and known:
        raise ContractError("invalid fixture unexpectedly uses a closed profile id")
    if expect_valid:
        if doc.get("schema") != "wellmanifest.auth-lifecycle/profile/v1":
            raise ContractError("valid fixture must use profile schema id")
        if doc.get("emitsMembershipSignal") is not True:
            raise ContractError("AUTHN-BOUND-001: membership signal required")
        authority = doc.get("authorityBoundary") or {}
        if authority.get("issuesGrants") is not False:
            raise ContractError("AuthN must not issue AuthZ grants")
        if authority.get("home") != "wellmanifest/authority-lifecycle":
            raise ContractError("authorityBoundary.home must xref authority-lifecycle")
        commercial = doc.get("commercialBoundary") or {}
        if commercial.get("processesPayment") is not False:
            raise ContractError("AUTHN-PAY-001: AuthN must not process payment")
        if commercial.get("consumesOnboardingProfile") != "membership-before-payment":
            raise ContractError("commercialBoundary must ADOPT membership-before-payment")
        if commercial.get("home") != "wellmanifest/saas-lifecycle":
            raise ContractError("commercialBoundary.home must xref saas-lifecycle")
        if profile_id == "otp-email":
            otp = doc.get("otpEmail") or {}
            if otp.get("channel") != "email":
                raise ContractError("otp-email profile requires otpEmail.channel=email")


def run() -> dict:
    for path in REQUIRED_DOCS:
        if not path.is_file():
            raise ContractError(f"missing required document: {path.relative_to(PACK)}")
    readme = (PACK / "README.md").read_text(encoding="utf-8")
    for profile in CLOSED_PROFILES:
        if f"`{profile}`" not in readme:
            raise ContractError(f"closed profile {profile} missing from README")
    for needle in (
        "wellmanifest/authority-lifecycle",
        "wellmanifest/saas-lifecycle",
        "membership-before-payment",
    ):
        if needle not in readme:
            raise ContractError(f"README missing cross-ref {needle}")
    version = (PACK / "VERSION").read_text(encoding="utf-8").strip()
    if version != "0.1.0-dev":
        raise ContractError("VERSION must be 0.1.0-dev for the skeleton")

    schema = load_json(PACK / "schemas/auth-lifecycle.schema.json")
    enum = (((schema.get("$defs") or {}).get("profileId") or {}).get("enum")) or []
    if list(enum) != list(CLOSED_PROFILES):
        raise ContractError("schema profileId enum must match CLOSED_PROFILES")

    valid = load_json(VALID_FIXTURE)
    check_profile_document(valid, expect_valid=True)
    invalid = load_json(INVALID_FIXTURE)
    check_profile_document(invalid, expect_valid=False)

    return {
        "schema": "wellmanifest.auth-lifecycle-conformance/v1",
        "ok": True,
        "profiles": list(CLOSED_PROFILES),
        "fixtures": {
            "valid": str(VALID_FIXTURE.relative_to(PACK)),
            "invalid_unknown_profile": str(INVALID_FIXTURE.relative_to(PACK)),
        },
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
