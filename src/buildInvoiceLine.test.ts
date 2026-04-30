import { describe, it, expect } from "vitest";
import { buildInvoiceLine } from "./buildInvoiceLine";

describe("buildInvoiceLine", () => {
  it("computes total and defaults meta to empty object", () => {
    const line = buildInvoiceLine({ sku: "WIDGET-01", qty: 3, price: 9.99 });

    expect(line).toEqual({
      sku: "WIDGET-01",
      total: 3 * 9.99,
      meta: {},
    });
  });

  it("passes through provided meta", () => {
    const line = buildInvoiceLine({
      sku: "GADGET-X",
      qty: 1,
      price: 25,
      meta: { warehouse: "US-EAST", fragile: true },
    });

    expect(line.sku).toBe("GADGET-X");
    expect(line.total).toBe(25);
    expect(line.meta).toEqual({ warehouse: "US-EAST", fragile: true });
  });

  it("throws on missing sku", () => {
    expect(() =>
      buildInvoiceLine({ sku: "", qty: 1, price: 10 }),
    ).toThrow();
  });

  it("throws on negative qty", () => {
    expect(() =>
      buildInvoiceLine({ sku: "A", qty: -1, price: 10 }),
    ).toThrow();
  });

  it("throws on non-integer qty", () => {
    expect(() =>
      buildInvoiceLine({ sku: "A", qty: 1.5, price: 10 }),
    ).toThrow();
  });

  it("throws on negative price", () => {
    expect(() =>
      buildInvoiceLine({ sku: "A", qty: 1, price: -5 }),
    ).toThrow();
  });

  it("throws when called with completely invalid input", () => {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    expect(() => buildInvoiceLine(42 as any)).toThrow();
  });
});
