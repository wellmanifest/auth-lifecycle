# AUTHN-FED-004

## Meaning

Errors or audit records cannot be diagnosed or correlated.

## Cause

Responses are not `application/problem+json`, no stable `code` list is declared, `traceparent` is not propagated, or failed sign-ins are not audited.

## Resolution

Return RFC 9457 problem details with a stable `code` and `request_id`, emit `traceparent`, include `WWW-Authenticate` on 401 and audit failures without secrets. See `docs/FEDERATION.md`.
