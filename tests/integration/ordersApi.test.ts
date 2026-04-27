import request from "supertest";
import { describe, expect, it } from "vitest";
import { createApp } from "../../src/app";

describe("orders API", () => {
  it("creates, reads, and updates an order", async () => {
    const app = createApp();

    const createResponse = await request(app)
      .post("/orders")
      .send({
        customerName: "Ada Lovelace",
        email: "ada@example.com",
        items: [
          { sku: "book", quantity: 2, unitPrice: 15 },
          { sku: "pen", quantity: 1, unitPrice: 5 },
        ],
        couponCode: "SAVE10",
      })
      .expect(201);

    expect(createResponse.body).toMatchObject({
      customerName: "Ada Lovelace",
      email: "ada@example.com",
      subtotal: 35,
      discount: 3.5,
      tax: 2.6,
      total: 34.1,
      status: "pending",
    });

    const id = createResponse.body.id;

    const readResponse = await request(app).get(`/orders/${id}`).expect(200);
    expect(readResponse.body.id).toBe(id);

    const updateResponse = await request(app).post(`/orders/${id}/pay`).expect(200);
    expect(updateResponse.body.status).toBe("paid");
  });

  it("returns validation errors with a consistent response shape", async () => {
    const app = createApp();

    const response = await request(app)
      .post("/orders")
      .send({
        customerName: "",
        email: "bad-email",
        items: [{ sku: "", quantity: 0, unitPrice: -1 }],
      })
      .expect(400);

    expect(response.body.error).toBe("Validation failed");
    expect(response.body.details.length).toBeGreaterThan(0);
  });

  it("returns 404 for unknown orders", async () => {
    const app = createApp();

    const response = await request(app).get("/orders/missing").expect(404);

    expect(response.body).toMatchObject({
      error: "Order missing was not found",
      code: "NOT_FOUND",
    });
  });
});
