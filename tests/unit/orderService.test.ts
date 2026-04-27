import { beforeEach, describe, expect, it } from "vitest";

import { InMemoryOrderRepository } from "../../src/repositories/inMemoryOrderRepository";
import { NotFoundError, ValidationError } from "../../src/domain/errors";
import { OrderService } from "../../src/domain/orderService";

describe("OrderService", () => {
  let repository: InMemoryOrderRepository;
  let service: OrderService;

  beforeEach(() => {
    repository = new InMemoryOrderRepository();
    service = new OrderService(repository);
  });

  it("creates an order with calculated totals and normalized values", async () => {
    const order = await service.createOrder({
      customerName: "Alice",
      email: "ALICE@example.COM",
      items: [
        { sku: " book-1 ", quantity: 2, unitPrice: 10 },
        { sku: "pen-2", quantity: 3, unitPrice: 2.5 }
      ]
    });

    expect(order).toMatchObject({
      email: "alice@example.com",
      status: "pending",
      subtotal: 27.5,
      discount: 0,
      tax: 2.27,
      total: 37.27
    });
    expect(order.items[0].sku).toBe("BOOK-1");
  });

  it("applies high-value discounts consistently", async () => {
    const order = await service.createOrder({
      customerName: "Buyer",
      email: "buyer@example.com",
      couponCode: "VIP20",
      items: [{ sku: "chair", quantity: 2, unitPrice: 100 }]
    });

    expect(order.subtotal).toBe(200);
    expect(order.discount).toBe(40);
    expect(order.tax).toBe(13.2);
    expect(order.total).toBe(173.2);
  });

  it("rejects duplicate SKUs so callers combine quantities explicitly", async () => {
    await expect(
      service.createOrder({
        customerName: "Active",
        email: "active@example.com",
        items: [
          { sku: "desk", quantity: 1, unitPrice: 50 },
          { sku: " DESK ", quantity: 1, unitPrice: 50 }
        ]
      })
    ).rejects.toBeInstanceOf(ValidationError);
  });

  it("marks an existing order as paid", async () => {
    const order = await service.createOrder({
      customerName: "Paid",
      email: "paid@example.com",
      items: [{ sku: "monitor", quantity: 1, unitPrice: 125 }]
    });

    const paidOrder = await service.payOrder(order.id);

    expect(paidOrder.status).toBe("paid");
  });

  it("throws a typed not-found error for missing orders", async () => {
    await expect(service.payOrder("missing-id")).rejects.toBeInstanceOf(NotFoundError);
  });
});
