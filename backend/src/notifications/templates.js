function escapeHtml(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

const templates = {
  'task.created': ({ title, dueAt }) => ({
    subject: `New task: ${title}`,
    body:
      `You created a task "${escapeHtml(title)}"` +
      (dueAt ? ` due at ${escapeHtml(dueAt)}.` : '.'),
  }),
  'task.completed': ({ title }) => ({
    subject: `Completed: ${title}`,
    body: `You marked "${escapeHtml(title)}" as done. Nice.`,
  }),
};

export function renderTemplate(name, payload) {
  const fn = templates[name];
  if (!fn) throw new Error(`unknown_template:${name}`);
  return fn(payload);
}
