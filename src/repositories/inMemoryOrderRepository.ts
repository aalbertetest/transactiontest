import { OrderRepository } from "./orderRepository";
import type { Order } from "../domain/order";

export class InMemoryOrderRepository implements OrderRepository {
  private orders = new Map<string, Order>();

  constructor(seedOrders: Order[] = []) {
    this.orders = new Map(seedOrders.map((order) => [order.id, order]));
  }

  async nextId(): Promise<string> {
    return `ord_${Date.now()}_${Math.random().toString(16).slice(2)}`;
  }

  async findAll(): Promise<Order[]> {
    return [...this.orders.values()];
  }

  async findById(id: string): Promise<Order | null> {
    return this.orders.get(id) ?? null;
  }

  async save(order: Order): Promise<Order> {
    this.orders.set(order.id, order);
    return order;
  }

  async reset(orders: Order[] = []): Promise<void> {
    this.orders = new Map(orders.map((order) => [order.id, order]));
  }
}
