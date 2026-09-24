# AUTHN-FED-001

## Meaning

The identity plane chooses its security role from a request header, or shares a process or data store with a relying application.

## Cause

`deployment.roleFromRequestHeaders` is not `false`, or `dedicatedProcess` / `dedicatedDataStore` is not `true`. Typical symptom: sign-in succeeds on the plane host but every later request is rejected by rules of the co-hosted application.

## Resolution

Run the identity plane as its own deployment with its own database and signing keys. Route its hostname to that deployment only. Do not branch on `Host` or `X-Forwarded-Host` to change the role. See `docs/FEDERATION.md`.
