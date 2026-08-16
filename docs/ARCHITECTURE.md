# Auth lifecycle architecture (draft)

AuthN profiles emit a membership-verified signal. AuthZ grants live in
`wellmanifest/authority-lifecycle`. Commercial activation stays in
`wellmanifest/saas-lifecycle` under an onboarding profile such as
`membership-before-payment`.

```text
otp-email / access-api / session-continue   ← HOME auth-lifecycle (AuthN)
        │ membership signal (binding receipt)
        ▼
membership-before-payment                   ← HOME saas-lifecycle (commercial)
        │ (only after membership)
        ▼
checkout / entitlement                      ← ADOPT offer + portal runtime

authority grants / leases                   ← HOME authority-lifecycle (AuthZ)
```

Normative schema: `schemas/auth-lifecycle.schema.json`. See `docs/SPEC.md`.
