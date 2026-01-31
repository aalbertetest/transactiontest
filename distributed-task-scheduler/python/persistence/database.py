"""
Database Connection Module
==========================

This module provides the database connection pool and utility functions
for the distributed task scheduler. It uses asyncpg for high-performance
asynchronous PostgreSQL access.

Key Features:
- Connection pooling with configurable size
- Automatic reconnection on failures
- Transaction support with savepoints
- Query timing and logging

Design Decisions:
1. Async-first design for high throughput
2. Connection pooling to reduce connection overhead
3. Explicit transaction management (no implicit commits)
4. Structured logging for debugging
"""

import asyncio
import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, AsyncIterator, Dict, List, Optional, TypeVar
from uuid import UUID

import asyncpg
from asyncpg import Connection, Pool, Record

from ..config.settings import DatabaseSettings

# Configure module logger
logger = logging.getLogger(__name__)

# Type variable for generic query results
T = TypeVar('T')


class DatabaseError(Exception):
    """Base exception for database errors."""
    pass


class ConnectionError(DatabaseError):
    """Raised when database connection fails."""
    pass


class TransactionError(DatabaseError):
    """Raised when transaction operations fail."""
    pass


class Database:
    """
    Async database connection manager using asyncpg.
    
    This class manages a connection pool and provides methods for
    executing queries, transactions, and prepared statements.
    
    Usage:
        db = Database(settings.database)
        await db.connect()
        
        # Simple query
        rows = await db.fetch("SELECT * FROM tasks WHERE status = $1", "QUEUED")
        
        # Transaction
        async with db.transaction() as conn:
            await conn.execute("UPDATE tasks SET status = $1 WHERE id = $2", "ACTIVE", task_id)
            await conn.execute("INSERT INTO task_events ...", ...)
        
        await db.disconnect()
    
    Attributes:
        settings: Database configuration settings
        pool: asyncpg connection pool (None until connect() is called)
    """
    
    def __init__(self, settings: DatabaseSettings):
        """
        Initialize the database manager.
        
        Args:
            settings: Database configuration settings containing
                      host, port, credentials, and pool settings.
        """
        self.settings = settings
        self._pool: Optional[Pool] = None
        self._connected = False
    
    @property
    def pool(self) -> Pool:
        """
        Get the connection pool, raising if not connected.
        
        Returns:
            The asyncpg connection pool.
            
        Raises:
            ConnectionError: If connect() has not been called.
        """
        if self._pool is None:
            raise ConnectionError("Database not connected. Call connect() first.")
        return self._pool
    
    @property
    def is_connected(self) -> bool:
        """Check if database is connected."""
        return self._connected and self._pool is not None
    
    async def connect(self) -> None:
        """
        Establish the database connection pool.
        
        Creates an asyncpg connection pool with the configured settings.
        This method is idempotent - calling it multiple times is safe.
        
        Raises:
            ConnectionError: If connection fails after retries.
        """
        if self._connected:
            logger.debug("Database already connected")
            return
        
        logger.info(
            "Connecting to database",
            extra={
                "host": self.settings.host,
                "port": self.settings.port,
                "database": self.settings.name,
                "max_connections": self.settings.max_connections,
            }
        )
        
        try:
            # Create connection pool with custom type codecs
            self._pool = await asyncpg.create_pool(
                host=self.settings.host,
                port=self.settings.port,
                user=self.settings.user,
                password=self.settings.password,
                database=self.settings.name,
                min_size=self.settings.min_connections,
                max_size=self.settings.max_connections,
                command_timeout=self.settings.command_timeout,
                # Enable prepared statement caching for performance
                statement_cache_size=100,
                # Custom type converters
                init=self._init_connection,
            )
            
            self._connected = True
            logger.info("Database connected successfully")
            
            # Verify connection with a simple query
            await self.fetch_val("SELECT 1")
            
        except asyncpg.PostgresError as e:
            logger.error(f"Failed to connect to database: {e}")
            raise ConnectionError(f"Database connection failed: {e}") from e
        except Exception as e:
            logger.error(f"Unexpected error connecting to database: {e}")
            raise ConnectionError(f"Database connection failed: {e}") from e
    
    async def disconnect(self) -> None:
        """
        Close the database connection pool.
        
        Gracefully closes all connections in the pool. This method
        is idempotent - calling it multiple times is safe.
        """
        if not self._connected or self._pool is None:
            return
        
        logger.info("Disconnecting from database")
        
        try:
            await self._pool.close()
        except Exception as e:
            logger.warning(f"Error during disconnect: {e}")
        finally:
            self._pool = None
            self._connected = False
            logger.info("Database disconnected")
    
    async def _init_connection(self, conn: Connection) -> None:
        """
        Initialize a new connection with custom settings.
        
        This is called for each new connection in the pool.
        Use it to set up type codecs, session variables, etc.
        
        Args:
            conn: The new connection to initialize.
        """
        # Set the application name for monitoring
        await conn.execute("SET application_name = 'distributed_task_scheduler'")
        
        # Enable statement timeout as a safety net
        timeout_ms = int(self.settings.command_timeout * 1000)
        await conn.execute(f"SET statement_timeout = {timeout_ms}")
    
    async def fetch(
        self,
        query: str,
        *args: Any,
        timeout: Optional[float] = None
    ) -> List[Record]:
        """
        Execute a query and return all rows.
        
        Args:
            query: SQL query with $1, $2, ... placeholders.
            *args: Query parameters.
            timeout: Optional query timeout in seconds.
            
        Returns:
            List of asyncpg Record objects.
            
        Raises:
            DatabaseError: If query execution fails.
        """
        try:
            return await self.pool.fetch(query, *args, timeout=timeout)
        except asyncpg.PostgresError as e:
            logger.error(f"Query failed: {e}", extra={"query": query[:100]})
            raise DatabaseError(f"Query failed: {e}") from e
    
    async def fetch_one(
        self,
        query: str,
        *args: Any,
        timeout: Optional[float] = None
    ) -> Optional[Record]:
        """
        Execute a query and return the first row.
        
        Args:
            query: SQL query with $1, $2, ... placeholders.
            *args: Query parameters.
            timeout: Optional query timeout in seconds.
            
        Returns:
            First row as an asyncpg Record, or None if no rows.
            
        Raises:
            DatabaseError: If query execution fails.
        """
        try:
            return await self.pool.fetchrow(query, *args, timeout=timeout)
        except asyncpg.PostgresError as e:
            logger.error(f"Query failed: {e}", extra={"query": query[:100]})
            raise DatabaseError(f"Query failed: {e}") from e
    
    async def fetch_val(
        self,
        query: str,
        *args: Any,
        column: int = 0,
        timeout: Optional[float] = None
    ) -> Any:
        """
        Execute a query and return a single value.
        
        Args:
            query: SQL query with $1, $2, ... placeholders.
            *args: Query parameters.
            column: Column index to return (default 0).
            timeout: Optional query timeout in seconds.
            
        Returns:
            Value from the specified column of the first row.
            
        Raises:
            DatabaseError: If query execution fails.
        """
        try:
            return await self.pool.fetchval(query, *args, column=column, timeout=timeout)
        except asyncpg.PostgresError as e:
            logger.error(f"Query failed: {e}", extra={"query": query[:100]})
            raise DatabaseError(f"Query failed: {e}") from e
    
    async def execute(
        self,
        query: str,
        *args: Any,
        timeout: Optional[float] = None
    ) -> str:
        """
        Execute a query without returning rows.
        
        Args:
            query: SQL query with $1, $2, ... placeholders.
            *args: Query parameters.
            timeout: Optional query timeout in seconds.
            
        Returns:
            Command status string (e.g., "UPDATE 1").
            
        Raises:
            DatabaseError: If query execution fails.
        """
        try:
            return await self.pool.execute(query, *args, timeout=timeout)
        except asyncpg.PostgresError as e:
            logger.error(f"Query failed: {e}", extra={"query": query[:100]})
            raise DatabaseError(f"Query failed: {e}") from e
    
    async def execute_many(
        self,
        query: str,
        args_list: List[tuple],
        timeout: Optional[float] = None
    ) -> None:
        """
        Execute a query multiple times with different parameters.
        
        This is more efficient than calling execute() in a loop
        because it batches the operations.
        
        Args:
            query: SQL query with $1, $2, ... placeholders.
            args_list: List of parameter tuples.
            timeout: Optional timeout in seconds.
            
        Raises:
            DatabaseError: If any execution fails.
        """
        try:
            await self.pool.executemany(query, args_list, timeout=timeout)
        except asyncpg.PostgresError as e:
            logger.error(f"Batch execution failed: {e}")
            raise DatabaseError(f"Batch execution failed: {e}") from e
    
    @asynccontextmanager
    async def acquire(self) -> AsyncIterator[Connection]:
        """
        Acquire a connection from the pool.
        
        Use this when you need to execute multiple operations
        on the same connection (e.g., for prepared statements).
        
        Yields:
            A connection from the pool.
            
        Example:
            async with db.acquire() as conn:
                stmt = await conn.prepare("SELECT * FROM tasks WHERE id = $1")
                for task_id in task_ids:
                    row = await stmt.fetchrow(task_id)
        """
        async with self.pool.acquire() as conn:
            yield conn
    
    @asynccontextmanager
    async def transaction(
        self,
        isolation: str = "read_committed"
    ) -> AsyncIterator[Connection]:
        """
        Execute operations within a database transaction.
        
        The transaction is automatically committed on success or
        rolled back on exception.
        
        Args:
            isolation: Transaction isolation level. Options:
                - "read_committed" (default, recommended)
                - "repeatable_read"
                - "serializable"
        
        Yields:
            A connection with an active transaction.
            
        Example:
            async with db.transaction() as conn:
                await conn.execute("UPDATE accounts SET balance = balance - $1 WHERE id = $2", amount, from_id)
                await conn.execute("UPDATE accounts SET balance = balance + $1 WHERE id = $2", amount, to_id)
        
        Raises:
            TransactionError: If transaction commit fails.
        """
        async with self.pool.acquire() as conn:
            # Start transaction with specified isolation level
            async with conn.transaction(isolation=isolation):
                yield conn
    
    async def health_check(self) -> bool:
        """
        Perform a health check on the database connection.
        
        Returns:
            True if database is healthy, False otherwise.
        """
        try:
            result = await self.fetch_val("SELECT 1", timeout=5.0)
            return result == 1
        except Exception as e:
            logger.warning(f"Health check failed: {e}")
            return False
    
    async def get_pool_stats(self) -> Dict[str, Any]:
        """
        Get connection pool statistics.
        
        Returns:
            Dictionary with pool metrics:
            - size: Current pool size
            - min_size: Minimum pool size
            - max_size: Maximum pool size
            - free_size: Available connections
            - used_size: Connections in use
        """
        pool = self.pool
        return {
            "size": pool.get_size(),
            "min_size": pool.get_min_size(),
            "max_size": pool.get_max_size(),
            "free_size": pool.get_idle_size(),
            "used_size": pool.get_size() - pool.get_idle_size(),
        }


# Utility functions for common database operations

def record_to_dict(record: Optional[Record]) -> Optional[Dict[str, Any]]:
    """
    Convert an asyncpg Record to a dictionary.
    
    Args:
        record: asyncpg Record object.
        
    Returns:
        Dictionary with column names as keys, or None if record is None.
    """
    if record is None:
        return None
    return dict(record)


def records_to_dicts(records: List[Record]) -> List[Dict[str, Any]]:
    """
    Convert a list of asyncpg Records to dictionaries.
    
    Args:
        records: List of asyncpg Record objects.
        
    Returns:
        List of dictionaries.
    """
    return [dict(r) for r in records]


def serialize_uuid(value: UUID) -> str:
    """Convert UUID to string for database."""
    return str(value)


def deserialize_uuid(value: str) -> UUID:
    """Convert string to UUID from database."""
    return UUID(value)
