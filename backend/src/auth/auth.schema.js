import { z } from 'zod';

export const credentialsSchema = z.object({
  email: z.string().email().max(254),
  password: z.string().min(12).max(200),
});

export const refreshSchema = z.object({
  refreshToken: z.string().min(10).max(200),
});
