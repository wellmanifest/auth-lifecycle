# AUTHN-FED-003

## Meaning

A partner refresh token or API token can leave the vault.

## Cause

`custody.exportRefreshToken` is not `false`, the vault is not envelope-encrypted, or consumers do not use token exchange or the broker proxy.

## Resolution

Keep partner credentials in the plane vault. Give consumers short-lived, downscoped tokens (RFC 8693) or proxy the call through the broker with an audit record. See `docs/FEDERATION.md`.
