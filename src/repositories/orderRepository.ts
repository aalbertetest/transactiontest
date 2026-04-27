import type { Order } from "../domain/order";

export interface OrderRepository {
  nextId(): Promise<string>;
  findAll(): Promise<Order[]>;
  findById(id: string): Promise<Order | null>;
  save(order: Order): Promise<Order>;
  reset(orders?: Order[]): Promise<void>;
}
