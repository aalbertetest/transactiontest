import type { ErrorRequestHandler } from "express";
import type { Logger } from "pino";
import { ZodError } from "zod";
import { AppError } from "../../domain/errors";

export function errorMiddleware(logger: Logger): ErrorRequestHandler {
  return (error, _req, res, _next) => {
    if (error instanceof ZodError) {
      res.status(400).json({
        error: "Validation failed",
        code: "VALIDATION_ERROR",
        details: error.errors,
      });
      return;
    }

    if (error instanceof AppError) {
      res.status(error.statusCode).json({
        error: error.message,
        code: error.code,
        details: error.details,
      });
      return;
    }

    logger.error({ error }, "Unhandled request failure");
    res.status(500).json({ error: "Internal server error", code: "INTERNAL_ERROR" });
  };
}
