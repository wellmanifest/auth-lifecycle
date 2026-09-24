# AUTHN-FED-005

## Meaning

A session cookie is shared across subdomains.

## Cause

`sessions.cookieScope` is not `host-only` or the cookie is not `HttpOnly`.

## Resolution

Issue host-only cookies (`__Host-` prefix over HTTPS). Relying applications obtain their own session through the OIDC code flow instead of reading the plane cookie. See `docs/FEDERATION.md`.
