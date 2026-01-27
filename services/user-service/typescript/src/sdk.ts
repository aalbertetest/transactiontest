import { z } from "zod";
import { retry } from "@dsp/common";

const UserSchema = z.object({
  id: z.string().min(1),
  email: z.string().email(),
  tenant_id: z.string().min(1).optional(),
  created_at: z.string().min(1).optional()
});
export type User = z.infer<typeof UserSchema>;

export class UserServiceClient {
  constructor(private readonly baseUrl: string, private readonly fetchImpl: typeof fetch = fetch) {}

  async me(accessToken: string): Promise<User> {
    return await retry(
      async () => {
        const r = await this.fetchImpl(`${this.baseUrl}/v1/users/me`, {
          method: "GET",
          headers: { Authorization: `Bearer ${accessToken}` }
        });
        const body = await r.json();
        if (!r.ok) throw new Error(`user me failed: ${r.status} ${JSON.stringify(body)}`);
        const out = UserSchema.safeParse(body);
        if (!out.success) throw new Error(`invalid user response: ${out.error.message}`);
        return out.data;
      },
      { maxAttempts: 3, baseDelayMs: 100, maxDelayMs: 1000, jitter: true }
    );
  }
}

