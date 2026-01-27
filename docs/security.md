Security
========

Threat Model
------------

Primary threats considered:

* Credential theft (phishing, token leakage)
* Man-in-the-middle attacks
* Replay attacks on payment APIs
* Injection attacks on data APIs
* Privilege escalation in service-to-service calls
* Denial-of-service via request floods

Security Controls
-----------------

* OAuth2 + JWT for authentication and authorization.
* MFA (TOTP) for privileged operations.
* TLS for all in-transit communication.
* Rate limiting and request validation at the gateway and services.
* Audit logging for sensitive actions.

TLS Setup
---------

* External TLS terminated at the API Gateway or ingress controller.
* Internal mTLS between services for identity and encryption.
* Use modern ciphersuites and disable TLS 1.0/1.1.

Key Rotation
------------

* JWT signing keys stored in KMS/Vault.
* Use key IDs (kid) in JWT headers.
* Rotate keys on a schedule; support overlapping keys for validation.
* Update gateway and auth service caches using background refresh.

Encryption at Rest
------------------

* Database encryption via disk-level or column-level encryption.
* Event logs and audit logs encrypted using KMS envelope encryption.
* Secret storage only in Vault/KMS, never plaintext in config.

Audit Logging
-------------

* All security-sensitive operations are logged:
  - Auth token issuance and refresh
  - Payment creation/capture/refund
  - Workflow start/termination
  - Admin configuration changes
* Logs include actor, action, resource, timestamp, and request correlation ID.

Least Privilege
---------------

* Service accounts are scoped to required resources.
* Separate roles for read, write, and admin operations.
* Production tokens are scoped by audience and resource.
