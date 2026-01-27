import { z } from "zod";

export type TenantId = string;
export type UserId = string;

export type UserRecord = {
  tenantId: TenantId;
  userId: UserId;
  email: string;
  passwordHash: string;
  totpSecret?: string;
  createdAt: string;
};

export const TokenRequestSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  mfa_code: z.string().min(4).optional()
});

export type TokenRequest = z.infer<typeof TokenRequestSchema>;

export const TokenResponseSchema = z.object({
  access_token: z.string().min(1),
  refresh_token: z.string().min(1),
  token_type: z.literal("bearer"),
  expires_in: z.number().int().positive()
});

export type TokenResponse = z.infer<typeof TokenResponseSchema>;

