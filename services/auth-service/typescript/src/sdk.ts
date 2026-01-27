import { z } from "zod";
import { retry } from "@dsp/common";

import { TokenRequestSchema, TokenResponseSchema, type TokenRequest, type TokenResponse } from "./models.js";

export class AuthServiceClient {
  constructor(private readonly baseUrl: string, private readonly fetchImpl: typeof fetch = fetch) {}

  async token(req: TokenRequest): Promise<TokenResponse> {
    const parsed = TokenRequestSchema.safeParse(req);
    if (!parsed.success) {
      throw new Error(`invalid token request: ${parsed.error.message}`);
    }

    return await retry(
      async () => {
        const r = await this.fetchImpl(`${this.baseUrl}/v1/auth/token`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(parsed.data)
        });
        const body = await r.json();
        if (!r.ok) throw new Error(`auth token failed: ${r.status} ${JSON.stringify(body)}`);

        const out = TokenResponseSchema.safeParse(body);
        if (!out.success) throw new Error(`invalid token response: ${out.error.message}`);
        return out.data;
      },
      { maxAttempts: 3, baseDelayMs: 100, maxDelayMs: 1000, jitter: true }
    );
  }

  async refresh(refreshToken: string): Promise<TokenResponse> {
    const Schema = z.object({ refresh_token: z.string().min(1) });
    const parsed = Schema.safeParse({ refresh_token: refreshToken });
    if (!parsed.success) throw new Error("invalid refresh token");

    return await retry(
      async () => {
        const r = await this.fetchImpl(`${this.baseUrl}/v1/auth/refresh`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(parsed.data)
        });
        const body = await r.json();
        if (!r.ok) throw new Error(`auth refresh failed: ${r.status} ${JSON.stringify(body)}`);

        const out = TokenResponseSchema.safeParse(body);
        if (!out.success) throw new Error(`invalid refresh response: ${out.error.message}`);
        return out.data;
      },
      { maxAttempts: 3, baseDelayMs: 100, maxDelayMs: 1000, jitter: true }
    );
  }
}

