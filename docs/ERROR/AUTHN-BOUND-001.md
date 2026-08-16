# AUTHN-BOUND-001

## Meaning

An AuthN document attempts to claim authority beyond identity and membership
binding.

## Cause

The document embeds authorization, billing entitlement, runtime credentials,
or another concern owned by a different lifecycle pack.

## Resolution

Keep only identity and membership evidence here. Reference the owning
Authority, SaaS, or Account Runtime contract for the other concern.
