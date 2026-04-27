/**
 * Subscribes to domain events on the bus and turns them into rows in the
 * `notifications` table. Knows about the `users` repo to resolve recipients,
 * and the `prefs` repo to honor per-user channel preferences.
 *
 * It does NOT know how to send anything — that's the worker's job.
 */
export function registerNotificationDispatcher({ bus, notes, prefs, users }) {
  bus.on('task.created', async ({ eventId, task }) => {
    if (!task.dueAt) return;
    enqueueFor({ eventId, eventName: 'task.created', task, notes, prefs, users });
  });

  bus.on('task.updated', async ({ eventId, before, after }) => {
    if (before.status !== 'done' && after.status === 'done') {
      enqueueFor({
        eventId,
        eventName: 'task.completed',
        task: after,
        notes,
        prefs,
        users,
      });
    }
  });
}

function enqueueFor({ eventId, eventName, task, notes, prefs, users }) {
  const userPrefs = prefs.get(task.userId);
  const channels = userPrefs.channelsFor(eventName);
  if (channels.length === 0) return;
  const user = users.findById(task.userId);
  if (!user) return;
  for (const channel of channels) {
    notes.enqueue({
      idempotencyKey: `${eventId}:${task.userId}:${channel}`,
      userId: task.userId,
      channel,
      template: eventName,
      payload: {
        taskId: task.id,
        title: task.title,
        dueAt: task.dueAt,
        recipient: user.email,
      },
    });
  }
}
