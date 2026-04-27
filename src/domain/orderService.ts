import { AppError, DuplicateResourceError, NotFoundError, ValidationError } from "./errors";
import type { OrderRepository } from "../repositories/orderRepository";
import { CreateOrderInput, Order, OrderLine, OrderStatus } from "./order";

const TAX_RATE = 0.0825;
const SHIPPING_FEE = 7.5;
const FREE_SHIPPING_THRESHOLD = 30;

export class OrderService {
  constructor(private readonly orders: OrderRepository) {}

  async listOrders(): Promise<Order[]> {
    return this.orders.findAll();
  }

  async getOrder(id: string): Promise<Order> {
    const order = await this.orders.findById(id);
    if (!order) {
      throw new NotFoundError(`Order ${id} was not found`);
    }

    return order;
  }

  async createOrder(input: CreateOrderInput): Promise<Order> {
    const email = input.email.trim().toLowerCase();
    const activeOrder = (await this.orders.findAll()).find(
      (order) =>
        order.email === email &&
        (order.status === "pending" || order.status === "paid"),
    );
    if (activeOrder) {
      throw new DuplicateResourceError("Customer already has an active order");
    }

    const lines = this.buildOrderLines(input);
    const subtotal = lines.reduce((sum, item) => sum + item.lineTotal, 0);
    const discount = this.calculateDiscount(subtotal, input.couponCode);
    const shippingFee = subtotal >= FREE_SHIPPING_THRESHOLD ? 0 : SHIPPING_FEE;
    const tax = this.roundMoney((subtotal - discount) * TAX_RATE);
    const total = this.roundMoney(subtotal - discount + shippingFee + tax);

    const order: Order = {
      id: await this.orders.nextId(),
      customerName: input.customerName.trim(),
      email,
      items: lines,
      subtotal,
      discount,
      tax,
      total,
      couponCode: input.couponCode,
      status: "pending",
      createdAt: new Date().toISOString(),
    };

    return this.orders.save(order);
  }

  async payOrder(id: string): Promise<Order> {
    const order = await this.getOrder(id);
    this.assertStatusTransition(order.status, "paid");

    return this.orders.save({
      ...order,
      status: "paid",
      paidAt: new Date().toISOString(),
    });
  }

  async cancelOrder(id: string): Promise<Order> {
    const order = await this.getOrder(id);
    this.assertStatusTransition(order.status, "cancelled");

    return this.orders.save({
      ...order,
      status: "cancelled",
      cancelledAt: new Date().toISOString(),
    });
  }

  async updateStatus(id: string, status: OrderStatus): Promise<Order> {
    if (status === "paid") {
      return this.payOrder(id);
    }

    if (status === "cancelled") {
      return this.cancelOrder(id);
    }

    const order = await this.getOrder(id);
    this.assertStatusTransition(order.status, status);

    return this.orders.save({
      ...order,
      status,
    });
  }

  private buildOrderLines(input: CreateOrderInput): OrderLine[] {
    const seen = new Set<string>();

    return input.items.map((item) => {
      const sku = item.sku.trim().toUpperCase();
      if (seen.has(sku)) {
        throw new ValidationError(`Duplicate SKU ${sku} should be combined before ordering`);
      }
      seen.add(sku);

      const lineTotal = this.roundMoney(item.unitPrice * item.quantity);
      return {
        sku,
        quantity: item.quantity,
        unitPrice: item.unitPrice,
        lineTotal,
      };
    });
  }

  private calculateDiscount(subtotal: number, couponCode?: string): number {
    const normalizedCoupon = couponCode?.trim().toUpperCase();
    if (normalizedCoupon === "SAVE10") {
      return this.roundMoney(subtotal * 0.1);
    }

    if (normalizedCoupon === "VIP20") {
      return this.roundMoney(subtotal * 0.2);
    }

    return 0;
  }

  private assertStatusTransition(current: OrderStatus, next: OrderStatus): void {
    if (current === next) {
      return;
    }

    const allowedTransitions: Record<OrderStatus, OrderStatus[]> = {
      pending: ["paid", "cancelled"],
      paid: ["shipped", "cancelled"],
      shipped: [],
      cancelled: [],
    };

    if (!allowedTransitions[current].includes(next)) {
      throw new AppError(
        `Order cannot transition from ${current} to ${next}`,
        409,
        "INVALID_STATUS_TRANSITION",
      );
    }
  }

  private roundMoney(value: number): number {
    return Math.round(value * 100) / 100;
  }
}
