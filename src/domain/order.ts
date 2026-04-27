export type OrderStatus = "pending" | "paid" | "shipped" | "cancelled";

export interface OrderItemInput {
  sku: string;
  quantity: number;
  unitPrice: number;
}

export interface OrderLine extends OrderItemInput {
  lineTotal: number;
}

export interface CreateOrderInput {
  customerName: string;
  email: string;
  items: OrderItemInput[];
  couponCode?: "SAVE10" | "VIP20";
}

export interface Order {
  id: string;
  customerName: string;
  email: string;
  items: OrderLine[];
  couponCode?: "SAVE10" | "VIP20";
  status: OrderStatus;
  subtotal: number;
  discount: number;
  tax: number;
  total: number;
  createdAt: string;
  paidAt?: string;
  cancelledAt?: string;
}
