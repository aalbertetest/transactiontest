import { z } from "zod";

export const lineItemSchema = z.object({
  sku: z.string().trim().min(1, "sku is required"),
  quantity: z.number().int().positive("quantity must be positive"),
  unitPrice: z.number().positive("unitPrice must be positive"),
});

export const createOrderSchema = z.object({
  customerName: z.string().trim().min(2, "customerName must be at least 2 characters"),
  email: z.string().trim().email("email must be valid"),
  couponCode: z.enum(["SAVE10", "VIP20"]).optional(),
  items: z.array(lineItemSchema).min(1, "at least one item is required"),
});

export const orderIdParamsSchema = z.object({
  id: z.string().trim().min(1, "id is required"),
});

export const updateStatusSchema = z.object({
  status: z.enum(["pending", "paid", "shipped", "cancelled"]),
});

export type CreateOrderInput = z.infer<typeof createOrderSchema>;
export type UpdateStatusInput = z.infer<typeof updateStatusSchema>;
