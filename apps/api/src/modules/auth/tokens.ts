import jwt, { type SignOptions } from "jsonwebtoken";
import { randomBytes, createHash } from "node:crypto";

import { prisma } from "../../db/prisma.js";
import { HttpError } from "../../http/errors.js";

export interface AccessTokenPayload {
  sub: string;
  email: string;
  name: string;
}

export interface RefreshTokenParts {
  token: string;
  tokenHash: string;
  expiresAt: Date;
}

export function signAccessToken(user: { id?: string; sub?: string; email: string; name: string }): string {
  const expiresIn = (process.env.ACCESS_TOKEN_TTL ?? "15m") as SignOptions["expiresIn"];
  const options: SignOptions = {
    expiresIn
  };

  return jwt.sign(
    { sub: user.id ?? user.sub, email: user.email, name: user.name },
    process.env.JWT_ACCESS_SECRET ?? "dev-access-token-secret-change-me",
    options
  );
}

export function verifyAccessToken(token: string): AccessTokenPayload {
  return jwt.verify(token, process.env.JWT_ACCESS_SECRET ?? "dev-access-token-secret-change-me") as AccessTokenPayload;
}

export function createRefreshTokenParts(): RefreshTokenParts {
  const token = randomBytes(48).toString("base64url");
  const tokenHash = hashRefreshToken(token);
  const refreshTokenTtlDays = Number(process.env.REFRESH_TOKEN_TTL_DAYS ?? 30);
  const expiresAt = new Date(Date.now() + refreshTokenTtlDays * 24 * 60 * 60 * 1000);

  return { token, tokenHash, expiresAt };
}

export async function createRefreshToken(userId: string): Promise<string> {
  const refresh = createRefreshTokenParts();
  await prisma.refreshToken.create({
    data: {
      tokenHash: refresh.tokenHash,
      userId,
      expiresAt: refresh.expiresAt
    }
  });
  return refresh.token;
}

export async function rotateRefreshToken(token: string): Promise<{
  token: string;
  user: { id: string; email: string; name: string };
}> {
  const tokenHash = hashRefreshToken(token);
  const stored = await prisma.refreshToken.findUnique({
    where: { tokenHash },
    include: { user: { select: { id: true, email: true, name: true } } }
  });

  if (!stored || stored.revokedAt || stored.expiresAt < new Date()) {
    throw new HttpError(401, "Invalid refresh token", "INVALID_REFRESH_TOKEN");
  }

  const nextToken = createRefreshTokenParts();
  await prisma.$transaction([
    prisma.refreshToken.update({
      where: { id: stored.id },
      data: { revokedAt: new Date(), replacedBy: nextToken.tokenHash }
    }),
    prisma.refreshToken.create({
      data: {
        tokenHash: nextToken.tokenHash,
        userId: stored.userId,
        expiresAt: nextToken.expiresAt
      }
    })
  ]);

  return { token: nextToken.token, user: stored.user };
}

export async function revokeRefreshToken(token: string): Promise<void> {
  await prisma.refreshToken.updateMany({
    where: { tokenHash: hashRefreshToken(token), revokedAt: null },
    data: { revokedAt: new Date() }
  });
}

export function hashRefreshToken(token: string): string {
  return createHash("sha256").update(token).digest("hex");
}
