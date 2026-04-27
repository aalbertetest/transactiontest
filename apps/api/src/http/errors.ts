import type { ErrorRequestHandler, NextFunction, Request, Response } from "express";

export class HttpError extends Error {
  constructor(
    public readonly statusCode: number,
    message: string,
    public readonly code = "API_ERROR",
  ) {
    super(message);
  }
}

export { HttpError as ApiError };

export function asyncHandler<T extends Request>(
  handler: (req: T, res: Response, next: NextFunction) => Promise<unknown>,
) {
  return (req: T, res: Response, next: NextFunction) => {
    void handler(req, res, next).catch(next);
  };
}

export function notFoundHandler(req: Request, _res: Response, next: NextFunction) {
  next(new HttpError(404, `Route not found: ${req.method} ${req.path}`, "NOT_FOUND"));
}

export const errorHandler: ErrorRequestHandler = (err, _req, res, _next) => {
  if (err instanceof HttpError) {
    res.status(err.statusCode).json({
      error: {
        code: err.code,
        message: err.message,
      },
    });
    return;
  }

  res.status(500).json({
    error: {
      code: "INTERNAL_SERVER_ERROR",
      message: "An unexpected error occurred",
    },
  });
};
