# VALIDATE

## Purpose

Validate Auth Lifecycle profile documents and their binding invariants without
performing authentication, issuing authority, or reading credentials.

## Syntax

```sh
python3 standard/conformance.py --all
```

## Inputs

- `schemas/auth-lifecycle.schema.json`;
- `schemas/auth-lifecycle.v1.gbnf`;
- `schemas/identity-federation.schema.json`;
- valid and invalid fixtures under `standard/fixtures/`.

## Outputs

A JSON conformance receipt with `ok: true`, bound artifact digests, supported
profiles, and the fixture paths that were evaluated.

## Errors

- `AUTHN-PROFILE-001` — the authentication profile is unknown.
- `AUTHN-BOUND-001` — membership binding exceeds the AuthN boundary.
- `AUTHN-PAY-001` — payment state is incorrectly treated as membership.
- `AUTHN-FED-001` … `AUTHN-FED-006` — identity plane or connector violates
  `docs/FEDERATION.md`.

## Examples

```sh
python3 standard/conformance.py --all
# {"ok": true, "schema": "wellmanifest.auth-lifecycle-conformance/v1", ...}
```
