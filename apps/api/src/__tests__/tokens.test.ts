import { describe, expect, it, vi } from "vitest";
import { createRefreshTokenParts, hashRefreshToken, signAccessToken, verifyAccessToken } from "../modules/auth/tokens.js";

vi.mock("../db/prisma.js", () => ({
  prisma: {}
}));

describe("token utilities", () => {
  it("signs verifiable access tokens", () => {
    const token = signAccessToken({ id: "user-1", email: "ada@example.com", name: "Ada" });
    expect(verifyAccessToken(token)).toMatchObject({
      sub: "user-1",
      email: "ada@example.com",
      name: "Ada"
    });
  });

  it("hashes refresh tokens without storing raw values", () => {
    const refresh = createRefreshTokenParts();
    expect(refresh.token).not.toEqual(refresh.tokenHash);
    expect(hashRefreshToken(refresh.token)).toEqual(refresh.tokenHash);
  });
});
