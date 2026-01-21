import { z } from "zod";
import { config } from "./config.js";

const stepSchema = z.object({
  id: z.string().min(1),
  type: z.enum(["http_request", "sleep", "echo"]),
  params: z.record(z.any()).optional(),
  depends_on: z.array(z.string()).optional()
});

export const workflowSpecSchema = z.object({
  steps: z.array(stepSchema).min(1)
});

export const createWorkflowSchema = z.object({
  name: z.string().min(1),
  description: z.string().optional(),
  spec: workflowSpecSchema
});

export const createWorkflowVersionSchema = z.object({
  spec: workflowSpecSchema
});

export const createWorkflowRunSchema = z.object({
  workflow_id: z.string().uuid(),
  input: z.record(z.any()).optional()
});

export function validateWorkflowSpec(spec: unknown): { ok: boolean; error?: string } {
  const parsed = workflowSpecSchema.safeParse(spec);
  if (!parsed.success) {
    return { ok: false, error: parsed.error.message };
  }

  if (parsed.data.steps.length > config.maxWorkflowSteps) {
    return { ok: false, error: "workflow exceeds max steps limit" };
  }

  const ids = new Set<string>();
  for (const step of parsed.data.steps) {
    if (ids.has(step.id)) {
      return { ok: false, error: `duplicate step id: ${step.id}` };
    }
    ids.add(step.id);
  }

  return { ok: true };
}
