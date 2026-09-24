# Ticket 004: Identity federation profile

Requested 2026-09-24 after the `user.clonerd.com.local` sign-in analysis: define
the identity, session, error and partner-connector standards before the
`clonerd-com/user-clonerd-com` implementation adopts them.

## Acceptance

- [x] `docs/FEDERATION.md` specifies OAuth 2.1 / OIDC, PKCE S256, device grant,
      DPoP, token exchange, RFC 9457 errors, trace context, sessions,
      deployment separation and partner connector custody.
- [x] `schemas/identity-federation.schema.json` with valid and invalid fixtures.
- [x] `AUTHN-FED-001` … `AUTHN-FED-006` runbooks and conformance checks.
- [x] `python3 standard/conformance.py --all` and `dsl_check.py validate` pass.
