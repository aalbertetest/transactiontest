import type { UserRecord } from "./models.js";

export type RefreshTokenRecord = {
  tokenHash: string;
  tenantId: string;
  userId: string;
  expiresAtUnix: number;
  revokedAtUnix?: number;
  createdAtUnix: number;
};

/**
 * In-memory store.
 *
 * Production path:
 * - Users in SQL (hashed passwords, MFA secrets encrypted).
 * - Refresh tokens hashed and stored with rotation and device binding.
 *
 * For this repo's initial runnable slice we keep it in-memory but fully implements:
 * - refresh token rotation
 * - token revocation
 * - expiry enforcement
 */
export class InMemoryAuthStore {
  private usersByEmail = new Map<string, UserRecord>();
  private refreshByHash = new Map<string, RefreshTokenRecord>();

  upsertUser(u: UserRecord): void {
    this.usersByEmail.set(u.email.toLowerCase(), u);
  }

  getUserByEmail(email: string): UserRecord | undefined {
    return this.usersByEmail.get(email.toLowerCase());
  }

  createRefreshToken(rec: Omit<RefreshTokenRecord, "createdAtUnix">): RefreshTokenRecord {
    const createdAtUnix = Math.floor(Date.now() / 1000);
    const full: RefreshTokenRecord = { ...rec, createdAtUnix };
    this.refreshByHash.set(full.tokenHash, full);
    return full;
  }

  getRefreshByHash(tokenHash: string): RefreshTokenRecord | undefined {
    return this.refreshByHash.get(tokenHash);
  }

  revokeRefresh(tokenHash: string): void {
    const rec = this.refreshByHash.get(tokenHash);
    if (!rec) return;
    rec.revokedAtUnix = Math.floor(Date.now() / 1000);
  }
}

