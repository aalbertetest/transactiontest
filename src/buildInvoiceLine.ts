import { z } from "zod";

export const InvoiceItemSchema = z.object({
  sku: z.string().min(1),
  qty: z.number().int().positive(),
  price: z.number().nonnegative(),
  meta: z.record(z.string(), z.unknown()).optional(),
});

export type InvoiceItem = z.infer<typeof InvoiceItemSchema>;

export interface InvoiceLine {
  sku: string;
  total: number;
  meta: Record<string, unknown>;
}

export function buildInvoiceLine(item: InvoiceItem): InvoiceLine {
  const parsed = InvoiceItemSchema.parse(item);

  return {
    sku: parsed.sku,
    total: parsed.qty * parsed.price,
    meta: parsed.meta ?? {},
  };
}
