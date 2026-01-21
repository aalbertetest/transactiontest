package scheduler

import (
	"context"
	"encoding/json"
	"errors"
	"log"
	"time"

	"github.com/jackc/pgx/v5/pgxpool"
)

// Scheduler coordinates workflow execution by scheduling ready steps into the queue.
type Scheduler struct {
	pool       *pgxpool.Pool
	config     Config
	leaderConn *pgxpool.Conn
}

// NewScheduler creates a scheduler with a PostgreSQL pool.
func NewScheduler(pool *pgxpool.Pool, config Config) *Scheduler {
	return &Scheduler{pool: pool, config: config}
}

// Run begins the scheduler loop.
func (s *Scheduler) Run(ctx context.Context) {
	ticker := time.NewTicker(s.config.PollInterval)
	defer ticker.Stop()

	for {
		select {
		case <-ctx.Done():
			s.releaseLeader()
			return
		case <-ticker.C:
			if s.ensureLeader(ctx) {
				start := time.Now()
				if err := s.scheduleOnce(ctx); err != nil {
					log.Printf("[scheduler] schedule error: %v", err)
				}
				SchedulerLoopDuration.Observe(time.Since(start).Seconds())
			}
		}
	}
}

// ensureLeader attempts to acquire leadership if not already leader.
func (s *Scheduler) ensureLeader(ctx context.Context) bool {
	if s.leaderConn != nil {
		_ = s.renewLease(ctx)
		return true
	}

	conn, err := s.pool.Acquire(ctx)
	if err != nil {
		log.Printf("[scheduler] failed to acquire conn for leader: %v", err)
		return false
	}

	var ok bool
	if err := conn.QueryRow(ctx, "SELECT pg_try_advisory_lock($1)", s.config.LeaderKey).Scan(&ok); err != nil || !ok {
		conn.Release()
		return false
	}

	s.leaderConn = conn
	if err := s.renewLease(ctx); err != nil {
		log.Printf("[scheduler] failed to renew lease: %v", err)
	}
	log.Printf("[scheduler] leader acquired by %s", s.config.SchedulerID)
	return true
}

func (s *Scheduler) renewLease(ctx context.Context) error {
	if s.leaderConn == nil {
		return nil
	}
	_, err := s.leaderConn.Exec(ctx,
		`INSERT INTO scheduler_leases (scheduler_id, lease_until, term)
         VALUES ($1, now() + $2::interval, 1)
         ON CONFLICT (scheduler_id)
         DO UPDATE SET lease_until = EXCLUDED.lease_until, term = scheduler_leases.term + 1`,
		s.config.SchedulerID,
		s.config.LeaseTTL.String(),
	)
	return err
}

func (s *Scheduler) releaseLeader() {
	if s.leaderConn == nil {
		return
	}
	_, _ = s.leaderConn.Exec(context.Background(), "SELECT pg_advisory_unlock($1)", s.config.LeaderKey)
	s.leaderConn.Release()
	s.leaderConn = nil
}

func (s *Scheduler) scheduleOnce(ctx context.Context) error {
	owned := ownedShardList(s.config.OwnedShards)
	if len(owned) == 0 {
		return errors.New("no shards owned")
	}

	rows, err := s.pool.Query(ctx,
		`SELECT id, workflow_id, version, status, input, shard_id
         FROM workflow_runs
         WHERE status IN ('pending', 'running')
           AND shard_id = ANY($1)
         ORDER BY created_at ASC
         LIMIT $2`,
		owned,
		s.config.MaxRunsPerLoop,
	)
	if err != nil {
		return err
	}
	defer rows.Close()

	for rows.Next() {
		var runID, workflowID, status string
		var version int
		var inputJSON []byte
		var shardID int
		if err := rows.Scan(&runID, &workflowID, &version, &status, &inputJSON, &shardID); err != nil {
			return err
		}
		SchedulerRunsProcessed.Inc()
		if err := s.scheduleRun(ctx, runID, workflowID, version, inputJSON); err != nil {
			log.Printf("[scheduler] run %s schedule error: %v", runID, err)
		}
	}
	return rows.Err()
}

func (s *Scheduler) scheduleRun(ctx context.Context, runID string, workflowID string, version int, inputJSON []byte) (err error) {
	tx, err := s.pool.Begin(ctx)
	if err != nil {
		return err
	}
	defer func() {
		if err != nil {
			_ = tx.Rollback(ctx)
		}
	}()

	var specBytes []byte
	if err = tx.QueryRow(ctx,
		`SELECT spec FROM workflow_versions WHERE workflow_id = $1 AND version = $2`,
		workflowID, version,
	).Scan(&specBytes); err != nil {
		return err
	}

	var spec WorkflowSpec
	if err = json.Unmarshal(specBytes, &spec); err != nil {
		return err
	}

	// Fetch current tasks for the run.
	taskRows, err := tx.Query(ctx,
		`SELECT step_id, status, attempt, max_attempts
         FROM tasks WHERE run_id = $1`,
		runID,
	)
	if err != nil {
		return err
	}
	defer taskRows.Close()

	stepStatus := map[string]string{}
	taskCount := 0
	hasFailed := false
	for taskRows.Next() {
		var stepID, status string
		var attempt, maxAttempts int
		if err = taskRows.Scan(&stepID, &status, &attempt, &maxAttempts); err != nil {
			return err
		}
		taskCount++
		stepStatus[stepID] = status
		if status == "failed" {
			hasFailed = true
		}
	}
	if err = taskRows.Err(); err != nil {
		return err
	}

	// If any step has failed we stop scheduling new work and allow the run to fail.
	readySteps := []WorkflowStep{}
	if !hasFailed {
		readySteps = readySteps(spec, stepStatus)
	}
	scheduled := 0
	for _, step := range readySteps {
		if _, exists := stepStatus[step.ID]; exists {
			continue
		}
		maxAttempts := parseMaxAttempts(step.Params)
		var payload []byte
		payload, err = json.Marshal(map[string]interface{}{
			"step":      step,
			"run_input": json.RawMessage(inputJSON),
		})
		if err != nil {
			return err
		}

		_, err = tx.Exec(ctx,
			`INSERT INTO tasks (run_id, step_id, status, attempt, max_attempts, run_after, payload, shard_id)
             VALUES ($1, $2, 'queued', 0, $3, now(), $4, $5)`,
			runID, step.ID, maxAttempts, payload, HashToShard(runID, s.config.ShardCount),
		)
		if err != nil {
			return err
		}
		scheduled++
		SchedulerTasksScheduled.Inc()
	}

	// Update run status based on task outcomes.
	runStatus, finished := resolveRunStatus(spec, stepStatus)
	if runStatus == "pending" && (scheduled > 0 || taskCount > 0) {
		runStatus = "running"
		_, err = tx.Exec(ctx,
			`UPDATE workflow_runs SET status = $1, started_at = COALESCE(started_at, now()) WHERE id = $2`,
			runStatus, runID,
		)
	} else if finished {
		_, err = tx.Exec(ctx,
			`UPDATE workflow_runs SET status = $1, finished_at = now() WHERE id = $2`,
			runStatus, runID,
		)
	}
	if err != nil {
		return err
	}

	if err = tx.Commit(ctx); err != nil {
		return err
	}
	return nil
}

// readySteps returns steps whose dependencies are all succeeded.
// This enforces the workflow DAG ordering.
func readySteps(spec WorkflowSpec, stepStatus map[string]string) []WorkflowStep {
	ready := make([]WorkflowStep, 0)
	for _, step := range spec.Steps {
		if len(step.DependsOn) == 0 {
			ready = append(ready, step)
			continue
		}
		allDone := true
		for _, dep := range step.DependsOn {
			if stepStatus[dep] != "succeeded" {
				allDone = false
				break
			}
		}
		if allDone {
			ready = append(ready, step)
		}
	}
	return ready
}

// resolveRunStatus determines whether a workflow is finished and with what status.
func resolveRunStatus(spec WorkflowSpec, stepStatus map[string]string) (string, bool) {
	allSucceeded := true
	for _, step := range spec.Steps {
		status, exists := stepStatus[step.ID]
		if !exists {
			allSucceeded = false
			continue
		}
		if status == "failed" {
			return "failed", true
		}
		if status != "succeeded" {
			allSucceeded = false
		}
	}
	if allSucceeded {
		return "succeeded", true
	}
	return "pending", false
}

func parseMaxAttempts(params map[string]interface{}) int {
	if params == nil {
		return 3
	}
	if value, ok := params["max_attempts"]; ok {
		if floatVal, ok := value.(float64); ok {
			if floatVal >= 1 && floatVal <= 20 {
				return int(floatVal)
			}
		}
	}
	return 3
}

func ownedShardList(owned map[int]bool) []int {
	shards := make([]int, 0, len(owned))
	for shard := range owned {
		shards = append(shards, shard)
	}
	return shards
}
