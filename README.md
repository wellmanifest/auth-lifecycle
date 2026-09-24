# wellmanifest/auth-lifecycle

Normative Wellmanifest domain pack for **authentication / membership binding**
profiles (OTP, magic-link, access-code, session bind) used before commercial
checkout.

Status: `0.1.0-dev` — closed AuthN vocabulary + schema stub.

## HOME vs ADOPT

- `HOME` wellmanifest · `shape` domain_pack
- Cross-refs (ADOPT, do not duplicate):
  - `wellmanifest/authority-lifecycle` — AuthZ grants, leases, revocation
  - `wellmanifest/account-runtime` — isolated tool runtimes without credential
    transfer
  - `wellmanifest/saas-lifecycle` — commercial state; consumes membership
    *signal* via onboarding profile `membership-before-payment`
  - `wellmanifest/poa` — plan / grant / receipt boundary for auth processes

### Boundary matrix (LC-030)

| Concern | HOME | Notes |
| --- | --- | --- |
| AuthN profile ids + binding receipts | **this pack** | `otp-email`, `access-api`, `session-continue` |
| AuthZ grants / leases / revoke | `authority-lifecycle` | ADOPT xref only |
| Isolated tool runtimes | `account-runtime` | Binding ≠ credential transfer |
| Commercial onboarding order | `saas-lifecycle` | Profile id `membership-before-payment` only |
| Portal OTP handlers | `subactor/www-sub-actor` | ADOPT profile ids; runtime implements |
| Identity plane, sessions, partner connectors | **this pack** | Identity federation profile (`docs/FEDERATION.md`) |

This pack owns AuthN profile vocabulary and fail-closed binding receipts. It
does not issue authority grants, process payments or provision tenants.

## Closed profile ids

| Profile id | Meaning |
| --- | --- |
| `otp-email` | One-time code to verified mailbox |
| `access-api` | Existing Control `/api/saas/access/*` bind |
| `session-continue` | Resume an already membership-verified session |

Unknown profile ids fail closed (`AUTHN-PROFILE-001`).

## Identity federation profile

`docs/FEDERATION.md` defines how a central identity plane (for example
`user.clonerd.com`) authenticates people and devices with OAuth 2.1 / OpenID
Connect, PKCE, the device grant and RFC 9457 errors, and how it keeps partner
credentials (GitHub, GitLab, Atlassian, Cloudflare) in a vault behind token
exchange or a broker proxy. Violations fail closed as `AUTHN-FED-001` …
`AUTHN-FED-006`.

## Artifacts

- Spec: `docs/SPEC.md`
- Schema: `schemas/auth-lifecycle.schema.json`
- GBNF: `schemas/auth-lifecycle.v1.gbnf`
- Federation spec: `docs/FEDERATION.md`
- Federation schema: `schemas/identity-federation.schema.json`
- Fixtures: `standard/fixtures/**`

## Conformance

```bash
python3 standard/conformance.py --all
```

Checks document digests, closed profile vocabulary, schema enum alignment,
valid `otp-email` fixture, and that unknown-profile fixtures stay outside the
closed set.

## Ticket

See `project/ticket-001/README.md` (bootstrap) and `project/ticket-002/`
(normative OTP schema).
