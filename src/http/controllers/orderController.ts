import type { Request, Response } from "express";
import { createOrderSchema, orderIdParamsSchema } from "../../validation/orderSchemas";
import type { OrderService } from "../../domain/orderService";

export class OrderController {
  constructor(private readonly orderService: OrderService) {}

  list = async (_req: Request, res: Response) => {
    const orders = await this.orderService.listOrders();
    res.json(orders);
  };

  getById = async (req: Request, res: Response) => {
    const { id } = orderIdParamsSchema.parse(req.params);
    const order = await this.orderService.getOrder(id);
    res.json(order);
  };

  create = async (req: Request, res: Response) => {
    const input = createOrderSchema.parse(req.body);
    const order = await this.orderService.createOrder(input);
    res.status(201).json(order);
  };

  pay = async (req: Request, res: Response) => {
    const { id } = orderIdParamsSchema.parse(req.params);
    const order = await this.orderService.payOrder(id);
    res.json(order);
  };

  cancel = async (req: Request, res: Response) => {
    const { id } = orderIdParamsSchema.parse(req.params);
    const order = await this.orderService.cancelOrder(id);
    res.json(order);
  };
}
