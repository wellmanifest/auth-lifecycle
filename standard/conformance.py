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
    PACK / "docs/FEDERATION.md",
    PACK / "schemas/identity-federation.schema.json",
)
VALID_FIXTURE = ROOT / "fixtures/valid/otp-email-profile.json"
INVALID_UNKNOWN = ROOT / "fixtures/invalid/unknown-profile.json"
INVALID_PAYMENT_AS_MEMBERSHIP = ROOT / "fixtures/invalid/payment-as-membership.json"

# Identity federation profile (docs/FEDERATION.md).
PLANE_SCHEMA = "wellmanifest.auth-lifecycle/identity-plane/v1"
CONNECTOR_SCHEMA = "wellmanifest.auth-lifecycle/connector/v1"
ALLOWED_GRANTS = (
    "authorization_code",
    "refresh_token",
    "urn:ietf:params:oauth:grant-type:device_code",
    "urn:ietf:params:oauth:grant-type:token-exchange",
)
CONNECTOR_AUTH_KINDS = (
    "oauth2-authorization-code-pkce",
    "github-app-installation",
    "atlassian-oauth2-3lo",
    "scoped-api-token",
)
WEBHOOK_VERIFICATION = ("hmac-sha256", "jwt", "shared-token")
FEDERATION_VALID = (
    ROOT / "fixtures/valid/identity-plane.json",
    ROOT / "fixtures/valid/connector-github.json",
    ROOT / "fixtures/valid/connector-gitlab.json",
    ROOT / "fixtures/valid/connector-atlassian.json",
    ROOT / "fixtures/valid/connector-cloudflare.json",
)
FEDERATION_INVALID = {
    ROOT / "fixtures/invalid/plane-role-from-host.json": "AUTHN-FED-001",
    ROOT / "fixtures/invalid/plane-password-grant.json": "AUTHN-FED-002",
    ROOT / "fixtures/invalid/connector-token-export.json": "AUTHN-FED-003",
    ROOT / "fixtures/invalid/plane-plain-errors.json": "AUTHN-FED-004",
    ROOT / "fixtures/invalid/plane-shared-cookie.json": "AUTHN-FED-005",
    ROOT / "fixtures/invalid/connector-unverified-webhook.json": "AUTHN-FED-006",
}


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


def receipt_deny_code(doc: dict) -> str | None:
    """Return fail-closed code if a binding receipt must be rejected."""
    if doc.get("schema") != "wellmanifest.auth-lifecycle/binding-receipt/v1":
        return "AUTHN-BOUND-001"
    if doc.get("membershipVerified") is not True:
        return "AUTHN-BOUND-001"
    if doc.get("paymentNotImplied") is not True:
        return "AUTHN-PAY-001"
    profile_id = doc.get("profileId")
    if profile_id not in CLOSED_PROFILES:
        return "AUTHN-PROFILE-001"
    return None


def plane_deny_code(doc: dict) -> str | None:
    deployment = doc.get("deployment") or {}
    if (deployment.get("roleFromRequestHeaders") is not False
            or deployment.get("dedicatedProcess") is not True
            or deployment.get("dedicatedDataStore") is not True):
        return "AUTHN-FED-001"
    protocol = doc.get("protocol") or {}
    grants = protocol.get("grantTypes") or []
    if (not grants or any(grant not in ALLOWED_GRANTS for grant in grants)
            or protocol.get("pkceMethods") != ["S256"]
            or protocol.get("oidcDiscovery") != "/.well-known/openid-configuration"):
        return "AUTHN-FED-002"
    errors = doc.get("errors") or {}
    if (errors.get("mediaType") != "application/problem+json" or not errors.get("codes")
            or errors.get("traceparent") is not True or protocol.get("problemDetails") is not True):
        return "AUTHN-FED-004"
    sessions = doc.get("sessions") or {}
    if sessions.get("cookieScope") != "host-only" or sessions.get("httpOnly") is not True:
        return "AUTHN-FED-005"
    audit = doc.get("audit") or {}
    if audit.get("failures") is not True or audit.get("secretsRedacted") is not True:
        return "AUTHN-FED-004"
    return None


def connector_deny_code(doc: dict) -> str | None:
    if doc.get("authKind") not in CONNECTOR_AUTH_KINDS:
        return "AUTHN-PROFILE-001"
    custody = doc.get("custody") or {}
    if (custody.get("vault") != "envelope-encrypted" or custody.get("exportRefreshToken") is not False
            or custody.get("consumerAccess") not in ("token-exchange", "broker-proxy")):
        return "AUTHN-FED-003"
    webhooks = doc.get("webhooks") or {}
    if webhooks.get("supported") and webhooks.get("verification") not in WEBHOOK_VERIFICATION:
        return "AUTHN-FED-006"
    return None


def federation_deny_code(doc: dict) -> str | None:
    """Return the fail-closed code for an identity plane or connector document."""
    if doc.get("schema") == PLANE_SCHEMA:
        return plane_deny_code(doc)
    if doc.get("schema") == CONNECTOR_SCHEMA:
        return connector_deny_code(doc)
    return "AUTHN-PROFILE-001"


def check_federation() -> None:
    schema = load_json(PACK / "schemas/identity-federation.schema.json")
    defs = schema.get("$defs") or {}
    if tuple((defs.get("grant") or {}).get("enum") or ()) != ALLOWED_GRANTS:
        raise ContractError("schema grant enum must match ALLOWED_GRANTS")
    if tuple((defs.get("authKind") or {}).get("enum") or ()) != CONNECTOR_AUTH_KINDS:
        raise ContractError("schema authKind enum must match CONNECTOR_AUTH_KINDS")
    for path in FEDERATION_VALID:
        code = federation_deny_code(load_json(path))
        if code is not None:
            raise ContractError(f"{path.relative_to(PACK)} must be valid, got {code}")
    for path, expected in FEDERATION_INVALID.items():
        code = federation_deny_code(load_json(path))
        if code != expected:
            raise ContractError(f"{path.relative_to(PACK)} must deny with {expected}, got {code!r}")


def assert_payment_as_membership_fixture(doc: dict) -> None:
    """Fixture must be shaped so receipt_deny_code returns AUTHN-PAY-001."""
    code = receipt_deny_code(doc)
    if code != "AUTHN-PAY-001":
        raise ContractError(
            f"payment-as-membership fixture must deny with AUTHN-PAY-001, got {code!r}"
        )


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
    unknown = load_json(INVALID_UNKNOWN)
    check_profile_document(unknown, expect_valid=False)
    payment_as_membership = load_json(INVALID_PAYMENT_AS_MEMBERSHIP)
    assert_payment_as_membership_fixture(payment_as_membership)
    check_federation()

    return {
        "schema": "wellmanifest.auth-lifecycle-conformance/v1",
        "ok": True,
        "profiles": list(CLOSED_PROFILES),
        "fixtures": {
            "valid": str(VALID_FIXTURE.relative_to(PACK)),
            "invalid_unknown_profile": str(INVALID_UNKNOWN.relative_to(PACK)),
            "invalid_payment_as_membership": str(
                INVALID_PAYMENT_AS_MEMBERSHIP.relative_to(PACK)
            ),
            "federation_valid": [str(path.relative_to(PACK)) for path in FEDERATION_VALID],
            "federation_invalid": {
                str(path.relative_to(PACK)): code for path, code in FEDERATION_INVALID.items()
            },
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
