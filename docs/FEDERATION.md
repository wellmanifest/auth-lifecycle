# Identity federation profile (v0.1.0-dev)

Normative profile for a **central identity plane** (for example
`user.clonerd.com`) that authenticates people and devices, hands identity to
relying applications and brokers access to partner systems (GitHub, GitLab,
Atlassian, Cloudflare and similar).

The profile standardises protocol shape, deployment separation, session
handling, error reporting and partner-credential custody. It does not issue
AuthZ grants (`wellmanifest/authority-lifecycle`), process payments
(`wellmanifest/saas-lifecycle`) or run tools with credentials
(`wellmanifest/account-runtime`).

Key words MUST, MUST NOT, SHOULD and MAY follow RFC 2119 / RFC 8174.

## 1. Documents

| Schema id | Purpose |
| --- | --- |
| `wellmanifest.auth-lifecycle/identity-plane/v1` | Declares one identity plane: issuer, deployment, grants, sessions, errors, audit, enterprise controls. |
| `wellmanifest.auth-lifecycle/connector/v1` | Declares one partner connector: auth kind, scopes, token custody, webhook verification. |

JSON Schema: `schemas/identity-federation.schema.json`. Conformance:
`python3 standard/conformance.py --all`.

## 2. Referenced standards

| Concern | Standard | Requirement |
| --- | --- | --- |
| Authorization framework | OAuth 2.1 (draft-ietf-oauth-v2-1), RFC 6749 | MUST |
| Browser sign-in | Authorization code + PKCE S256 (RFC 7636) | MUST |
| Identity layer | OpenID Connect Core 1.0, Discovery 1.0 | MUST |
| Signing keys | JWKS (RFC 7517), JWT (RFC 7519), algorithms `EdDSA` or `ES256` | MUST |
| Devices / CLI / desktop | Device Authorization Grant (RFC 8628) | MUST when devices are served |
| Sender-constrained tokens | DPoP (RFC 9449) | SHOULD (MUST for offline leases) |
| Service-to-service downscoping | Token Exchange (RFC 8693) | SHOULD |
| Token revocation / introspection | RFC 7009 / RFC 7662 | SHOULD |
| Server metadata | RFC 8414 | MUST (via OIDC discovery) |
| HTTP errors | Problem Details (RFC 9457) | MUST |
| Correlation | W3C Trace Context `traceparent` | MUST |
| Enterprise SSO (upstream) | OIDC federation; SAML 2.0 | SHOULD for enterprise tier |
| Provisioning | SCIM 2.0 (RFC 7643/7644) | SHOULD for enterprise tier |
| Strong authentication | WebAuthn Level 2 / passkeys; TOTP (RFC 6238) | SHOULD |

Forbidden grants: `password` (resource owner password credentials) and
`implicit`. A plane that offers either fails `AUTHN-FED-002`.

## 3. Deployment separation

1. The identity plane MUST run as its own deployment with its own data store
   and signing keys. It MUST NOT share a process or database with a relying
   application.
2. A process MUST NOT change its security role (identity plane vs relying
   application) based on `Host`, `X-Forwarded-Host` or any other
   client-influenced header. Violations fail `AUTHN-FED-001`.
3. Forwarded headers are trusted only from an explicit proxy allowlist.
4. The issuer URL is fixed per deployment. A development plane (for example
   `https://user.clonerd.com.local`) MUST NOT point devices at a production
   issuer.

## 4. Relying applications

1. Relying applications (for example `app.clonerd.com`) are OIDC clients using
   the backend-for-frontend pattern: the code exchange happens server-side and
   the browser receives an application-host session cookie.
2. Session cookies MUST be host-only (`__Host-` prefix when served over
   HTTPS), `HttpOnly`, `Secure`, `SameSite=Lax` or stricter. A session cookie
   with a `Domain` attribute shared across subdomains fails `AUTHN-FED-005`.
3. Sessions declare an absolute lifetime, an idle timeout and rotation on
   privilege change. Users can list and revoke their sessions.
4. State-changing browser requests carry a CSRF token or rely on
   `SameSite=Strict` together with an `Origin` allowlist of exact origins
   (no suffix matching such as `*.local`).

## 5. Error and audit profile

1. Every 4xx/5xx response from the plane and from relying applications MUST be
   `application/problem+json` with a stable, machine-readable `code`
   (for example `invalid_credentials`, `session_missing`,
   `device_not_activated`, `lease_expired`), `status`, `title`, and an
   `instance` or `request_id`. A single human message shared by several
   causes fails `AUTHN-FED-004`.
2. `401` responses MUST include `WWW-Authenticate`.
3. Every response carries `traceparent` (echoed or generated) and the request
   id. Clients log `status`, `code`, `request_id` and path, never an opaque
   object.
4. Clients stop dependent data requests after the session probe fails instead
   of fanning out requests that fail for the same reason.
5. Audit events MUST cover success **and** failure of sign-in, registration,
   MFA, device approval, token refresh reuse, connector link/unlink and
   connector token use. Audit records never contain secrets or tokens.

## 6. Partner connectors

1. Each partner is declared by a connector document. Adding a partner is a new
   document, not a change to the plane's code path.
2. Closed auth kinds:
   `oauth2-authorization-code-pkce`, `github-app-installation`,
   `atlassian-oauth2-3lo`, `scoped-api-token`.
   Unknown kinds fail closed as `AUTHN-PROFILE-001`.
3. Custody: partner refresh tokens and API tokens stay in the plane's vault
   (envelope encryption, key reference outside the database). Consumers
   receive only short-lived, downscoped tokens (RFC 8693) or call a broker
   proxy that audits each request. A connector whose `custody.exportRefreshToken`
   is not `false` fails `AUTHN-FED-003`.
4. Scopes are least privilege and declared per connector; requesting a scope
   outside the declared set is refused.
5. Inbound webhooks MUST be verified (HMAC signature, JWT or shared token as
   the partner defines) before any processing. An unverified webhook
   declaration fails `AUTHN-FED-006`.
6. Link and unlink are explicit user actions with revocation at the partner
   when the partner supports it.

Recommended defaults:

| Partner | Auth kind | Notes |
| --- | --- | --- |
| GitHub | `github-app-installation` | Installation tokens (1 h), fine-grained permissions, HMAC webhooks. |
| GitLab (SaaS / self-managed) | `oauth2-authorization-code-pkce` | Configurable base URL, rotating refresh tokens, webhook secret token. |
| Atlassian (Jira, Confluence) | `atlassian-oauth2-3lo` | Rotating refresh tokens, site id from accessible resources. |
| Cloudflare | `scoped-api-token` | Minimal token permissions per account or zone. |

## 7. Fail-closed codes

| Code | Meaning |
| --- | --- |
| `AUTHN-FED-001` | Security role chosen from a request header or plane co-hosted with a relying application |
| `AUTHN-FED-002` | Non-standard or forbidden grant (`password`, `implicit`, code without PKCE S256) |
| `AUTHN-FED-003` | Partner refresh/API token leaves the vault |
| `AUTHN-FED-004` | Errors without RFC 9457 problem details and stable codes |
| `AUTHN-FED-005` | Session cookie shared across subdomains |
| `AUTHN-FED-006` | Webhook accepted without verification |
