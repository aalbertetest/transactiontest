import express from "express";
import { randomUUID } from "crypto";
import { config } from "./config.js";
import { pool, withClient } from "./db.js";
import {
  createWorkflowSchema,
  createWorkflowRunSchema,
  createWorkflowVersionSchema,
  validateWorkflowSpec
} from "./validation.js";
import { httpRequestDuration, register } from "./metrics.js";

const app = express();
app.use(express.json({ limit: `${config.maxPayloadBytes}b` }));

app.use((req, res, next) => {
  const end = httpRequestDuration.startTimer({ method: req.method, path: req.path });
  res.on("finish", () => {
    end({ status: res.statusCode });
  });
  next();
});

// hashToShard assigns a stable shard for a given run ID.
// This ensures API, scheduler, and executor agree on the shard mapping.
function hashToShard(id: string, shardCount: number): number {
  let hash = 2166136261;
  for (let i = 0; i < id.length; i += 1) {
    hash ^= id.charCodeAt(i);
    hash = (hash * 16777619) >>> 0;
  }
  return hash % shardCount;
}

function sendError(res: express.Response, code: string, message: string, details?: Record<string, unknown>) {
  return res.status(400).json({ error: { code, message, details } });
}

app.get("/v1/health", (_req, res) => res.status(200).json({ status: "ok" }));

app.get("/metrics", async (_req, res) => {
  res.set("Content-Type", register.contentType);
  res.end(await register.metrics());
});

// Create a workflow and its initial version in a single transaction.
app.post("/v1/workflows", async (req, res) => {
  const parsed = createWorkflowSchema.safeParse(req.body);
  if (!parsed.success) {
    return sendError(res, "invalid_request", parsed.error.message);
  }

  const { name, description, spec } = parsed.data;
  const specCheck = validateWorkflowSpec(spec);
  if (!specCheck.ok) {
    return sendError(res, "invalid_request", specCheck.error || "invalid spec");
  }

  try {
    const created = await withClient(async (client) => {
      await client.query("BEGIN");
      const workflow = await client.query(
        `INSERT INTO workflows (name, description)
         VALUES ($1, $2)
         RETURNING id, name, description, active, created_at, updated_at`,
        [name, description || null]
      );
      await client.query(
        `INSERT INTO workflow_versions (workflow_id, version, spec)
         VALUES ($1, 1, $2)`,
        [workflow.rows[0].id, spec]
      );
      await client.query("COMMIT");
      return workflow.rows[0];
    });
    return res.status(201).json(created);
  } catch (err) {
    return sendError(res, "db_error", "failed to create workflow", { reason: String(err) });
  }
});

app.get("/v1/workflows", async (_req, res) => {
  try {
    const result = await pool.query(
      "SELECT id, name, description, active, created_at, updated_at FROM workflows ORDER BY created_at DESC"
    );
    return res.status(200).json({ workflows: result.rows });
  } catch (err) {
    return sendError(res, "db_error", "failed to list workflows", { reason: String(err) });
  }
});

app.get("/v1/workflows/:id", async (req, res) => {
  try {
    const result = await pool.query(
      "SELECT id, name, description, active, created_at, updated_at FROM workflows WHERE id = $1",
      [req.params.id]
    );
    if (result.rowCount === 0) {
      return res.status(404).json({ error: { code: "not_found", message: "workflow not found" } });
    }
    return res.status(200).json(result.rows[0]);
  } catch (err) {
    return sendError(res, "db_error", "failed to get workflow", { reason: String(err) });
  }
});

// Create a new immutable version of an existing workflow.
app.post("/v1/workflows/:id/versions", async (req, res) => {
  const parsed = createWorkflowVersionSchema.safeParse(req.body);
  if (!parsed.success) {
    return sendError(res, "invalid_request", parsed.error.message);
  }

  const specCheck = validateWorkflowSpec(parsed.data.spec);
  if (!specCheck.ok) {
    return sendError(res, "invalid_request", specCheck.error || "invalid spec");
  }

  try {
    const version = await withClient(async (client) => {
      await client.query("BEGIN");
      const current = await client.query(
        "SELECT COALESCE(MAX(version), 0) as version FROM workflow_versions WHERE workflow_id = $1",
        [req.params.id]
      );
      const newVersion = Number(current.rows[0].version) + 1;
      const inserted = await client.query(
        `INSERT INTO workflow_versions (workflow_id, version, spec)
         VALUES ($1, $2, $3)
         RETURNING id, workflow_id, version, spec, created_at`,
        [req.params.id, newVersion, parsed.data.spec]
      );
      await client.query("UPDATE workflows SET updated_at = now() WHERE id = $1", [req.params.id]);
      await client.query("COMMIT");
      return inserted.rows[0];
    });
    return res.status(201).json(version);
  } catch (err) {
    return sendError(res, "db_error", "failed to create workflow version", { reason: String(err) });
  }
});

// Trigger a workflow run using the latest workflow version.
app.post("/v1/workflow-runs", async (req, res) => {
  const parsed = createWorkflowRunSchema.safeParse(req.body);
  if (!parsed.success) {
    return sendError(res, "invalid_request", parsed.error.message);
  }

  try {
    const runId = randomUUID();
    const shardId = hashToShard(runId, parseInt(process.env.SHARD_COUNT || "16", 10));
    const run = await withClient(async (client) => {
      await client.query("BEGIN");
      const version = await client.query(
        "SELECT version FROM workflow_versions WHERE workflow_id = $1 ORDER BY version DESC LIMIT 1",
        [parsed.data.workflow_id]
      );
      if (version.rowCount === 0) {
        await client.query("ROLLBACK");
        return null;
      }
      const inserted = await client.query(
        `INSERT INTO workflow_runs (id, workflow_id, version, status, input, shard_id)
         VALUES ($1, $2, $3, 'pending', $4, $5)
         RETURNING id, workflow_id, version, status, input, output, created_at, started_at, finished_at, shard_id`,
        [runId, parsed.data.workflow_id, version.rows[0].version, parsed.data.input || null, shardId]
      );
      await client.query("COMMIT");
      return inserted.rows[0];
    });

    if (!run) {
      return res.status(404).json({ error: { code: "not_found", message: "workflow not found" } });
    }

    return res.status(201).json(run);
  } catch (err) {
    return sendError(res, "db_error", "failed to create workflow run", { reason: String(err) });
  }
});

app.get("/v1/workflow-runs/:id", async (req, res) => {
  try {
    const result = await pool.query(
      `SELECT id, workflow_id, version, status, input, output, created_at, started_at, finished_at, shard_id
       FROM workflow_runs WHERE id = $1`,
      [req.params.id]
    );
    if (result.rowCount === 0) {
      return res.status(404).json({ error: { code: "not_found", message: "run not found" } });
    }
    return res.status(200).json(result.rows[0]);
  } catch (err) {
    return sendError(res, "db_error", "failed to get workflow run", { reason: String(err) });
  }
});

app.get("/v1/workflow-runs/:id/tasks", async (req, res) => {
  try {
    const result = await pool.query(
      `SELECT id, run_id, step_id, status, attempt, max_attempts, run_after, payload, created_at, updated_at
       FROM tasks WHERE run_id = $1 ORDER BY created_at ASC`,
      [req.params.id]
    );
    return res.status(200).json({ tasks: result.rows });
  } catch (err) {
    return sendError(res, "db_error", "failed to list tasks", { reason: String(err) });
  }
});

app.post("/v1/workflow-runs/:id/cancel", async (req, res) => {
  try {
    await withClient(async (client) => {
      await client.query("BEGIN");
      await client.query(
        `UPDATE workflow_runs
         SET status = 'cancelled', finished_at = now()
         WHERE id = $1 AND status IN ('pending','running')`,
        [req.params.id]
      );
      await client.query(
        `UPDATE tasks
         SET status = 'failed', updated_at = now()
         WHERE run_id = $1 AND status IN ('queued','running')`,
        [req.params.id]
      );
      await client.query("COMMIT");
    });
    return res.status(202).json({ status: "cancelled" });
  } catch (err) {
    return sendError(res, "db_error", "failed to cancel workflow run", { reason: String(err) });
  }
});

app.use((err: Error, _req: express.Request, res: express.Response, _next: express.NextFunction) => {
  return res.status(500).json({ error: { code: "internal_error", message: err.message } });
});

app.listen(config.port, () => {
  // eslint-disable-next-line no-console
  console.log(`[api] listening on ${config.port}`);
});
