"""
Distributed Task Scheduler - Python Implementation
===================================================

A production-grade distributed task scheduling system with support for:
- Immediate and scheduled task execution
- Cron-based job scheduling
- Distributed worker coordination
- Automatic retry with exponential backoff
- Dead letter queue for failed tasks

Example usage:
    from scheduler import TaskScheduler, Worker

    # Start scheduler
    scheduler = TaskScheduler.from_config('config.yaml')
    await scheduler.start()

    # Start worker
    worker = Worker.from_config('config.yaml')
    worker.register_handler('send_email', send_email_handler)
    await worker.start()

    # Submit task
    task = await scheduler.submit(
        task_type='send_email',
        payload={'to': 'user@example.com'},
        priority=50
    )
"""

__version__ = "1.0.0"
__author__ = "Distributed Systems Team"

from .scheduler.scheduler import TaskScheduler
from .worker.worker import Worker
from .queue.task_queue import TaskQueue
from .persistence.repository import TaskRepository
from .config.settings import Settings

__all__ = [
    "TaskScheduler",
    "Worker",
    "TaskQueue",
    "TaskRepository",
    "Settings",
]
