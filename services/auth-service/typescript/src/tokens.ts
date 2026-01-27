import { SignJWT, jwtVerify, type JWTPayload } from "jose";

export type JwtSigner = {
  signAccessToken: (payload: JWTPayload, ttlSeconds: number) => Promise<string>;
};

export type JwtVerifier = {
  verify: (token: string) => Promise<JWTPayload>;
};

function toKeyList(secretsCsv: string): Uint8Array[] {
  const parts = secretsCsv
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean);
  if (parts.length === 0) {
    throw new Error("DSP_JWT_SECRETS must not be empty");
  }
  return parts.map((s) => new TextEncoder().encode(s));
}

/**
 * HS256 signer/verifier with multi-key verification for rotation.
 *
 * - First secret is signing key.
 * - All secrets are accepted for verification.
 */
export function createHs256Jwt(secretsCsv: string, opts: { issuer: string; audience: string; kid: string }): {
  signer: JwtSigner;
  verifier: JwtVerifier;
} {
  const keys = toKeyList(secretsCsv);
  const signingKey = keys[0];

  return {
    signer: {
      async signAccessToken(payload: JWTPayload, ttlSeconds: number): Promise<string> {
        const now = Math.floor(Date.now() / 1000);
        return await new SignJWT(payload)
          .setProtectedHeader({ alg: "HS256", kid: opts.kid, typ: "JWT" })
          .setIssuedAt(now)
          .setIssuer(opts.issuer)
          .setAudience(opts.audience)
          .setExpirationTime(now + ttlSeconds)
          .sign(signingKey);
      }
    },
    verifier: {
      async verify(token: string): Promise<JWTPayload> {
        // Try each key to support rotation without downtime.
        let lastErr: unknown = undefined;
        for (const k of keys) {
          try {
            const { payload } = await jwtVerify(token, k, {
              issuer: opts.issuer,
              audience: opts.audience
            });
            return payload;
          } catch (err) {
            lastErr = err;
          }
        }
        throw lastErr;
      }
    }
  };
}

