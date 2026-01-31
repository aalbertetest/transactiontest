// Package persistence provides database access for the distributed task scheduler.
//
// This package uses pgx for high-performance PostgreSQL access with:
//   - Connection pooling
//   - Prepared statement caching
//   - Transaction support
//   - Context-aware operations
package persistence

import (
	"context"
	"fmt"
	"sync"
	"time"

	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/rs/zerolog/log"

	"github.com/distributed-task-scheduler/internal/config"
)

// Database provides database access using a connection pool.
type Database struct {
	pool   *pgxpool.Pool
	config config.DatabaseConfig
	mu     sync.RWMutex
}

// NewDatabase creates a new database connection manager.
func NewDatabase(cfg config.DatabaseConfig) *Database {
	return &Database{
		config: cfg,
	}
}

// Connect establishes the database connection pool.
func (db *Database) Connect(ctx context.Context) error {
	db.mu.Lock()
	defer db.mu.Unlock()

	if db.pool != nil {
		return nil // Already connected
	}

	log.Info().
		Str("host", db.config.Host).
		Int("port", db.config.Port).
		Str("database", db.config.Name).
		Int("max_connections", db.config.MaxConnections).
		Msg("Connecting to database")

	// Build connection config
	poolConfig, err := pgxpool.ParseConfig(db.config.DSN())
	if err != nil {
		return fmt.Errorf("failed to parse database config: %w", err)
	}

	// Configure pool
	poolConfig.MaxConns = int32(db.config.MaxConnections)
	poolConfig.MinConns = int32(db.config.MinConnections)
	poolConfig.MaxConnLifetime = time.Hour
	poolConfig.MaxConnIdleTime = 30 * time.Minute
	poolConfig.HealthCheckPeriod = time.Minute

	// Connection initialization
	poolConfig.AfterConnect = func(ctx context.Context, conn *pgx.Conn) error {
		// Set application name for monitoring
		_, err := conn.Exec(ctx, "SET application_name = 'distributed_task_scheduler'")
		return err
	}

	// Create pool
	pool, err := pgxpool.NewWithConfig(ctx, poolConfig)
	if err != nil {
		return fmt.Errorf("failed to create connection pool: %w", err)
	}

	// Verify connection
	if err := pool.Ping(ctx); err != nil {
		pool.Close()
		return fmt.Errorf("failed to ping database: %w", err)
	}

	db.pool = pool
	log.Info().Msg("Database connected successfully")

	return nil
}

// Close closes the database connection pool.
func (db *Database) Close() {
	db.mu.Lock()
	defer db.mu.Unlock()

	if db.pool != nil {
		db.pool.Close()
		db.pool = nil
		log.Info().Msg("Database disconnected")
	}
}

// Pool returns the underlying connection pool.
func (db *Database) Pool() *pgxpool.Pool {
	db.mu.RLock()
	defer db.mu.RUnlock()
	return db.pool
}

// Exec executes a query without returning rows.
func (db *Database) Exec(ctx context.Context, sql string, args ...interface{}) error {
	_, err := db.pool.Exec(ctx, sql, args...)
	if err != nil {
		return fmt.Errorf("exec failed: %w", err)
	}
	return nil
}

// QueryRow executes a query that returns at most one row.
func (db *Database) QueryRow(ctx context.Context, sql string, args ...interface{}) pgx.Row {
	return db.pool.QueryRow(ctx, sql, args...)
}

// Query executes a query that returns rows.
func (db *Database) Query(ctx context.Context, sql string, args ...interface{}) (pgx.Rows, error) {
	return db.pool.Query(ctx, sql, args...)
}

// BeginTx starts a new transaction.
func (db *Database) BeginTx(ctx context.Context) (pgx.Tx, error) {
	return db.pool.Begin(ctx)
}

// WithTx executes a function within a transaction.
// The transaction is committed on success or rolled back on error.
func (db *Database) WithTx(ctx context.Context, fn func(tx pgx.Tx) error) error {
	tx, err := db.pool.Begin(ctx)
	if err != nil {
		return fmt.Errorf("failed to begin transaction: %w", err)
	}

	defer func() {
		if p := recover(); p != nil {
			tx.Rollback(ctx)
			panic(p) // Re-throw panic after rollback
		}
	}()

	if err := fn(tx); err != nil {
		if rbErr := tx.Rollback(ctx); rbErr != nil {
			log.Error().Err(rbErr).Msg("Failed to rollback transaction")
		}
		return err
	}

	if err := tx.Commit(ctx); err != nil {
		return fmt.Errorf("failed to commit transaction: %w", err)
	}

	return nil
}

// HealthCheck performs a health check on the database connection.
func (db *Database) HealthCheck(ctx context.Context) error {
	db.mu.RLock()
	defer db.mu.RUnlock()

	if db.pool == nil {
		return fmt.Errorf("database not connected")
	}

	ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
	defer cancel()

	return db.pool.Ping(ctx)
}

// Stats returns connection pool statistics.
func (db *Database) Stats() *pgxpool.Stat {
	db.mu.RLock()
	defer db.mu.RUnlock()

	if db.pool == nil {
		return nil
	}

	return db.pool.Stat()
}
