import type { NextFunction, Request, Response } from "express";
import type { AccessTokenPayload } from "../modules/auth/tokens.js";
import { HttpError } from "./errors.js";
import { verifyAccessToken } from "../modules/auth/tokens.js";

export interface AuthenticatedRequest extends Request {
  user?: AccessTokenPayload;
}

export function requireAuth(req: AuthenticatedRequest, _res: Response, next: NextFunction) {
  const header = req.header("authorization");
  const token = header?.startsWith("Bearer ") ? header.slice("Bearer ".length) : undefined;

  if (!token) {
    return next(new HttpError(401, "Missing bearer token", "UNAUTHENTICATED"));
  }

  try {
    req.user = verifyAccessToken(token);
    return next();
  } catch {
    return next(new HttpError(401, "Invalid or expired access token", "UNAUTHENTICATED"));
  }
}
