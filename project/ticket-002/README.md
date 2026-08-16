# Ticket 002: Normative AuthN schemas (LC-010)

## Intent

Publish minimal normative AuthN artifacts for `otp-email` (plus closed siblings)
with explicit ADOPT edges to AuthZ and commercial onboarding.

## Acceptance criteria

- [x] AC-01: `schemas/auth-lifecycle.schema.json` declares closed profile ids.
- [x] AC-02: GBNF sketch exists at `schemas/auth-lifecycle.v1.gbnf`.
- [x] AC-03: Valid `otp-email` fixture + invalid unknown-profile fixture.
- [x] AC-04: Docs cross-ref `authority-lifecycle` and saas
      `membership-before-payment`.
- [x] AC-05: `python3 standard/conformance.py --all` passes.

## Out of scope

- www OTP UI / MX stack (`ticket-otp-email-login`)
- Full IdP at auth.subactor.com
- Payment-as-membership negative fixture suite beyond stub (follow-up)
