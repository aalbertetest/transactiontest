import express from "express";
import type { Logger } from "pino";
import { asyncHandler } from "./http/asyncHandler";
import { errorMiddleware } from "./http/middleware/errorMiddleware";
import { requestLogger } from "./http/middleware/requestLogger";
import { OrderService } from "./domain/orderService";
import { InMemoryOrderRepository } from "./repositories/inMemoryOrderRepository";
import { OrderController } from "./http/controllers/orderController";
import { createLogger } from "./logging/logger";

export function createApp(options?: { logger?: Logger }) {
  const logger = options?.logger ?? createLogger();
  const orderRepository = new InMemoryOrderRepository();
  const orderService = new OrderService(orderRepository);
  const orderController = new OrderController(orderService);

  const app = express();
  app.use(express.json());
  app.use(requestLogger(logger));

  app.get("/health", (_req, res) => {
    res.json({ status: "ok" });
  });

  app.post("/orders", asyncHandler(orderController.create));
  app.get("/orders/:id", asyncHandler(orderController.getById));
  app.post("/orders/:id/pay", asyncHandler(orderController.pay));
  app.post("/orders/:id/cancel", asyncHandler(orderController.cancel));

  app.use(errorMiddleware(logger));

  return app;
}
