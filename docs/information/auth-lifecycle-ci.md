---
{
  "schema": "wellmanifest.docs/document/v1",
  "id": "auth-lifecycle-ci",
  "kind": "information",
  "version": 1,
  "title": "Auth Lifecycle conformance in pull requests",
  "status": "proposed",
  "owner": "wellmanifest/auth-lifecycle",
  "created": "2026-09-24",
  "updated": "2026-09-24",
  "review_after": "2026-10-24",
  "source_revision": "2189d5ab5808667abadeb6a0eaefb7307e4560d5",
  "affected_repositories": ["wellmanifest/auth-lifecycle"],
  "evidence": ["https://github.com/wellmanifest/auth-lifecycle/blob/2189d5ab5808667abadeb6a0eaefb7307e4560d5/standard/conformance.py"]
}
---

# Auth Lifecycle conformance in pull requests

<!-- docs:section purpose -->
## Purpose

Run Auth Lifecycle conformance as a named `conformance` check on pull requests
and pushes to `main` before independent Validator publication.

<!-- docs:section scope -->
## Scope

This document owns the CI check in `wellmanifest/auth-lifecycle`. The protected
Validator registry and a future OneDev verification profile have separate
owners and deployment receipts.

<!-- docs:section evidence -->
## Evidence

The baseline conformance command passes at source revision
`2189d5ab5808667abadeb6a0eaefb7307e4560d5`. The hosted workflow status and
Validator terminal receipt must be observed for each exact PR head; this file
is not publication evidence.

<!-- docs:section content -->
## Check contract

`.github/workflows/conformance.yml` checks out the PR merge result with full
history and runs `python3 standard/conformance.py --all`. The Validator profile
must require `conformance` for this repository before the coding agent requests
publication. A check that never ran is not green.

<!-- docs:section limitations -->
## Limitations

GitHub Actions capacity or billing may prevent this check from running. The
workflow alone does not configure OneDev or protect `main`; a reviewed policy
migration requires a deployed OneDev profile and a successful exact-head/base
canary before changing required contexts.

<!-- docs:section next_actions -->
## Next actions

Add an explicit protected Validator registry profile requiring `conformance`,
then validate and merge the CI PR through that identity. If the workflow fails
on valid fixtures, repair it on the ticket branch and rerun the exact-head check.
