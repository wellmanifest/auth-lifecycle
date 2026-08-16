# Auth lifecycle normative spec (v0.1.0-dev)

## Ownership

| Concern | HOME | Notes |
| --- | --- | --- |
| AuthN profile ids + binding receipts | **this pack** | `otp-email`, `access-api`, `session-continue` |
| AuthZ grants / leases / revoke | `wellmanifest/authority-lifecycle` | ADOPT xref only |
| Commercial onboarding order | `wellmanifest/saas-lifecycle` | Consumes membership **signal**; profile id `membership-before-payment` |
| Isolated tool runtimes | `wellmanifest/account-runtime` | Binding ≠ credential transfer |

## Fail-closed codes

| Code | Meaning |
| --- | --- |
| `AUTHN-PROFILE-001` | Unknown or undeclared AuthN profile id |
| `AUTHN-BOUND-001` | Binding receipt missing membership-verified signal |
| `AUTHN-PAY-001` | Payment / checkout treated as membership (denied here; saas owns `SAAS-ONBOARD-*`) |

## Artifacts

- JSON Schema: `schemas/auth-lifecycle.schema.json`
- GBNF sketch: `schemas/auth-lifecycle.v1.gbnf`
- Fixtures: `standard/fixtures/valid|invalid/**`

Runtime portals (e.g. `subactor/www-sub-actor`) ADOPT profile ids; they do not
redefine the closed vocabulary.
