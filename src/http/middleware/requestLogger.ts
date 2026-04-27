import type { NextFunction, Request, Response } from "express";
import type { Logger } from "pino";

export function requestLogger(logger: Logger) {
  return (req: Request, res: Response, next: NextFunction) => {
    const startedAt = Date.now();

    res.on("finish", () => {
      logger.info(
        {
          method: req.method,
          path: req.path,
          statusCode: res.statusCode,
          durationMs: Date.now() - startedAt,
        },
        "request completed",
      );
    });

    next();
  };
}
