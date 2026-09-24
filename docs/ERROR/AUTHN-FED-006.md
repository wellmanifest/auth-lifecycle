# AUTHN-FED-006

## Meaning

A partner webhook is accepted without verification.

## Cause

`webhooks.supported` is `true` without a `verification` method.

## Resolution

Declare and enforce `hmac-sha256`, `jwt` or `shared-token` verification as the partner defines before processing the payload. See `docs/FEDERATION.md`.
