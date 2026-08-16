# AUTHN-PAY-001

## Meaning

Payment or subscription state is being used as proof of membership.

## Cause

The input binds a user to an organization because a payment, plan, invoice, or
checkout record exists.

## Resolution

Use explicit AuthN membership evidence. Treat commercial state as a separate
SaaS Lifecycle fact and never infer identity binding from payment.
