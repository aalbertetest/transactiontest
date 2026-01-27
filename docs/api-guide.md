API Guide
=========

Authentication
--------------

1) OAuth2 Authorization Code:
* Call /auth/oauth/authorize to get a code
* Call /auth/oauth/token to exchange for an access token
* Send Authorization: Bearer <token> on all requests

2) MFA:
* Call /auth/mfa/enroll to get a secret and QR URI
* Call /auth/mfa/verify with a code from your authenticator

Client SDK Usage (Python)
-------------------------

from src.python.platform import AuthClient, UserClient

auth = AuthClient("http://localhost:8081")
token = auth.token(code="auth_code", client_id="platform_cli", client_secret="platform_secret")

user = UserClient("http://localhost:8082")
user.register(email="alice@example.com", display_name="Alice")

Client SDK Usage (Go)
---------------------

auth := AuthClient{http: HttpClient{BaseURL: "http://localhost:8081"}}
token, _ := auth.Token("auth_code", "platform_cli", "platform_secret")

user := UserClient{http: HttpClient{BaseURL: "http://localhost:8082"}}
user.Register("alice@example.com", "Alice")

Client SDK Usage (TypeScript)
-----------------------------

const auth = new AuthClient(new HttpClient("http://localhost:8081"));
const token = await auth.token("auth_code", "platform_cli", "platform_secret");

const user = new UserClient(new HttpClient("http://localhost:8082"));
await user.register("alice@example.com", "Alice");

Gateway Usage
-------------

All services are accessible through the API gateway (default port 8080).
Configure clients to talk to the gateway for centralized auth and routing.

Example (curl):

curl -X POST http://localhost:8080/users/register \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","display_name":"Alice"}'
