import { z } from 'zod';

export const taskStatus = z.enum(['todo', 'doing', 'done']);

export const createTaskSchema = z.object({
  title: z.string().min(1).max(200),
  description: z.string().max(10_000).optional(),
  status: taskStatus.default('todo'),
  dueAt: z.string().datetime().optional(),
});

export const updateTaskSchema = z
  .object({
    title: z.string().min(1).max(200),
    description: z.string().max(10_000).nullable(),
    status: taskStatus,
    dueAt: z.string().datetime().nullable(),
  })
  .partial();

export const listTasksQuery = z.object({
  status: taskStatus.optional(),
  cursor: z.string().optional(),
  limit: z.coerce.number().int().min(1).max(100).default(20),
});
