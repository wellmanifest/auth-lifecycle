# Ticket 005: Publish an Auth Lifecycle conformance check

- **ID**: ticket-005
- **Owner**: user continuation in this session
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-09-24

## Goal and scope

The user directed independent OneDev and Validator review. This repository has
conformance code but no hosted workflow, protected check or Validator profile.
Create a real `conformance` PR check first; a separate Validator registry ticket
must require it before this PR can be published through that identity. This
stage does not claim a deployed OneDev profile or waive another check.

## Acceptance criteria

- [ ] AC-01: `conformance` executes on PR merge result and on `main` using the
      repository's dependency-free conformance command.
- [ ] AC-02: The check runs on the exact PR head before Validator approval;
      a separate protected profile requires it.
- [ ] AC-03: Canonical CI documentation is indexed and local conformance passes.

## Tracking boundary

The canonical operational description is `docs/information/auth-lifecycle-ci.md`.
Raw receipts remain in ignored recovery storage.
