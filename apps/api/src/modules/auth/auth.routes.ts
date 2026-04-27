import { Router } from "express";
import { prisma } from "../../db/prisma.js";
import { requireAuth } from "../../http/auth-middleware.js";
import { asyncHandler } from "../../http/async-handler.js";
import { HttpError } from "../../http/errors.js";
import { hashPassword, verifyPassword } from "./password.js";
import {
  createRefreshToken,
  hashRefreshToken,
  revokeRefreshToken,
  rotateRefreshToken,
  signAccessToken,
} from "./tokens.js";

const router = Router();

function userPayload(user: { id: string; email: string; name: string }) {
  return { id: user.id, email: user.email, name: user.name };
}

router.post(
  "/register",
  asyncHandler(async (req, res) => {
    const { email, password, name } = req.body as {
      email?: string;
      password?: string;
      name?: string;
    };

    if (!email || !password || !name) {
      throw new HttpError(400, "email, password, and name are required", "VALIDATION_ERROR");
    }
    if (password.length < 8) {
      throw new HttpError(400, "password must be at least 8 characters", "VALIDATION_ERROR");
    }

    const existing = await prisma.user.findUnique({ where: { email } });
    if (existing) {
      throw new HttpError(409, "email is already registered", "EMAIL_TAKEN");
    }

    const user = await prisma.user.create({
      data: {
        email: email.toLowerCase(),
        name,
        passwordHash: await hashPassword(password)
      }
    });

    const payload = userPayload(user);
    res.status(201).json({
      user: payload,
      accessToken: signAccessToken(user),
      refreshToken: await createRefreshToken(user.id)
    });
  })
);

router.post(
  "/login",
  asyncHandler(async (req, res) => {
    const { email, password } = req.body as { email?: string; password?: string };
    if (!email || !password) {
      throw new HttpError(400, "email and password are required", "VALIDATION_ERROR");
    }

    const user = await prisma.user.findUnique({ where: { email: email.toLowerCase() } });
    if (!user || !(await verifyPassword(password, user.passwordHash))) {
      throw new HttpError(401, "invalid credentials", "INVALID_CREDENTIALS");
    }

    res.json({
      user: userPayload(user),
      accessToken: signAccessToken(user),
      refreshToken: await createRefreshToken(user.id)
    });
  })
);

router.post(
  "/refresh",
  asyncHandler(async (req, res) => {
    const { refreshToken } = req.body as { refreshToken?: string };
    if (!refreshToken) {
      throw new HttpError(400, "refreshToken is required", "VALIDATION_ERROR");
    }

    const rotated = await rotateRefreshToken(refreshToken);
    res.json({
      accessToken: signAccessToken(rotated.user),
      refreshToken: rotated.token
    });
  })
);

router.post(
  "/logout",
  requireAuth,
  asyncHandler(async (req, res) => {
    const { refreshToken } = req.body as { refreshToken?: string };
    if (refreshToken) {
      await revokeRefreshToken(refreshToken);
    }
    res.status(204).send();
  })
);

router.get(
  "/me",
  requireAuth,
  asyncHandler(async (req, res) => {
    const user = await prisma.user.findUniqueOrThrow({ where: { id: req.user!.sub } });
    res.json({ user: userPayload(user) });
  })
);

export { router as authRouter };
