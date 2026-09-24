# AUTHN-FED-002

## Meaning

The plane offers a non-standard or forbidden grant.

## Cause

`protocol.grantTypes` contains `password`, `implicit` or an unknown grant, PKCE is not exactly `S256`, or OIDC discovery is missing.

## Resolution

Offer authorization code + PKCE S256 for browsers, the device grant (RFC 8628) for devices and refresh tokens with rotation. Publish `/.well-known/openid-configuration`. See `docs/FEDERATION.md`.
