# wellmanifest/auth-lifecycle

Normative Wellmanifest domain pack for **authentication / membership binding**
profiles (OTP, magic-link, access-code, session bind) used before commercial
checkout.

Status: `0.1.0-dev` skeleton. Governed implementation pending.

## HOME vs ADOPT

- `HOME` wellmanifest · `shape` domain_pack
- Cross-refs (ADOPT, do not duplicate):
  - `wellmanifest/authority-lifecycle` — AuthZ grants, leases, revocation
  - `wellmanifest/account-runtime` — isolated tool runtimes without credential
    transfer
  - `wellmanifest/saas-lifecycle` — commercial state; consumes membership
    *signal* via onboarding profile `membership-before-payment`
  - `wellmanifest/poa` — plan / grant / receipt boundary for auth processes

This pack owns AuthN profile vocabulary and fail-closed binding receipts. It
does not issue authority grants, process payments or provision tenants.

## Closed profile ids (draft)

| Profile id | Meaning |
| --- | --- |
| `otp-email` | One-time code to verified mailbox |
| `access-api` | Existing Control `/api/saas/access/*` bind |
| `session-continue` | Resume an already membership-verified session |

Unknown profile ids fail closed (`AUTHN-PROFILE-001`).

## Conformance

```bash
python3 standard/conformance.py --all
```

The stub currently checks document digests and closed profile vocabulary only.

## Ticket

See `project/ticket-001/README.md`.
