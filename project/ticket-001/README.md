# Ticket 001: Bootstrap auth-lifecycle domain pack

## Intent

Create `wellmanifest/auth-lifecycle` as the AuthN counterpart to
`wellmanifest/authority-lifecycle` (AuthZ), so SaaS onboarding can ADOPT
`membership-before-payment` without embedding OTP rules in commercial
lifecycle docs.

## Acceptance criteria

- [ ] AC-01: Repository exists under `wellmanifest/auth-lifecycle` with
      `HOME wellmanifest` / `shape domain_pack` placement.
- [ ] AC-02: Closed draft profile vocabulary documented (`otp-email`,
      `access-api`, `session-continue`) with fail-closed unknown-id behavior.
- [ ] AC-03: Cross-refs to authority-lifecycle, account-runtime, saas-lifecycle
      and poa are ADOPT-only (no duplicated grant/payment rules).
- [ ] AC-04: `standard/conformance.py --all` passes as a digest/vocabulary stub.
- [ ] AC-05: Adopt `wellmanifest/new-project` governance baseline.

## Out of scope

- Implementing Control OTP handlers
- Merging `ticket-otp-email-login` into www-sub-actor
- Payment or authority grant semantics
