import type { NextFunction, Request, Response } from "express";

type AsyncRoute = (req: Request, res: Response, next: NextFunction) => Promise<void>;

export function asyncHandler(route: AsyncRoute): AsyncRoute {
  return async (req, res, next) => {
    try {
      await route(req, res, next);
    } catch (error) {
      next(error);
    }
  };
}
