# Auth lifecycle normative spec (v0.1.0-dev)

## Ownership

| Concern | HOME | Notes |
| --- | --- | --- |
| AuthN profile ids + binding receipts | **this pack** | `otp-email`, `access-api`, `session-continue` |
| AuthZ grants / leases / revoke | `wellmanifest/authority-lifecycle` | ADOPT xref only (see pack README LC-030) |
| Commercial onboarding order | `wellmanifest/saas-lifecycle` | Consumes membership **signal**; profile id `membership-before-payment` |
| Isolated tool runtimes | `wellmanifest/account-runtime` | Binding ≠ credential transfer (see pack README LC-030) |

## Fail-closed codes

| Code | Meaning |
| --- | --- |
| `AUTHN-PROFILE-001` | Unknown or undeclared AuthN profile id |
| `AUTHN-BOUND-001` | Binding receipt missing membership-verified signal |
| `AUTHN-PAY-001` | Payment / checkout treated as membership (denied here; saas owns `SAAS-ONBOARD-*`) |
| `AUTHN-FED-001` | Identity plane role taken from request headers or co-hosted with a relying application |
| `AUTHN-FED-002` | Non-standard or forbidden grant (`password`, `implicit`, no PKCE S256) |
| `AUTHN-FED-003` | Partner refresh/API token leaves the vault |
| `AUTHN-FED-004` | Errors without RFC 9457 problem details, stable codes or failure audit |
| `AUTHN-FED-005` | Session cookie shared across subdomains |
| `AUTHN-FED-006` | Webhook accepted without verification |

## Identity federation

The identity plane and partner connector documents are specified in
`docs/FEDERATION.md` and `schemas/identity-federation.schema.json`.

## Artifacts

- JSON Schema: `schemas/auth-lifecycle.schema.json`
- GBNF sketch: `schemas/auth-lifecycle.v1.gbnf`
- Fixtures: `standard/fixtures/valid|invalid/**`

Runtime portals (e.g. `subactor/www-sub-actor`) ADOPT profile ids; they do not
redefine the closed vocabulary.
