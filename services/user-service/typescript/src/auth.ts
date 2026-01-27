import { jwtVerify, type JWTPayload } from "jose";

function toKeyList(secretsCsv: string): Uint8Array[] {
  const parts = secretsCsv
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean);
  if (parts.length === 0) throw new Error("DSP_JWT_SECRETS must not be empty");
  return parts.map((s) => new TextEncoder().encode(s));
}

export function createJwtVerifier(secretsCsv: string, opts: { issuer: string; audience: string }) {
  const keys = toKeyList(secretsCsv);
  return {
    async verify(token: string): Promise<JWTPayload> {
      let lastErr: unknown = undefined;
      for (const k of keys) {
        try {
          const { payload } = await jwtVerify(token, k, { issuer: opts.issuer, audience: opts.audience });
          return payload;
        } catch (err) {
          lastErr = err;
        }
      }
      throw lastErr;
    }
  };
}

