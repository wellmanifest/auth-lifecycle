# AUTHN-PROFILE-001

## Meaning

The document names an authentication profile outside the closed profile set.

## Cause

`profile` is not one of `otp-email`, `access-api`, or `session-continue`.

## Resolution

Select a declared profile or version the Auth Lifecycle contract before using a
new profile name. Do not silently map unknown profiles.
