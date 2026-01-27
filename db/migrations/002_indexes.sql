-- Indexes and partition helpers

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_payment_intents_idempotency ON payment_intents(idempotency_key);
CREATE INDEX idx_queue_messages_poll ON queue_messages(queue_name, visible_at);
CREATE INDEX idx_workflow_runs_status ON workflow_runs(workflow_id, status);
CREATE INDEX idx_scheduled_tasks_run_at ON scheduled_tasks(run_at);

-- Example partitioning strategy notes (vendor-specific)
-- Stream records are typically sharded/partitioned by topic and partition.
-- Queue messages can be partitioned by queue_name hash.
