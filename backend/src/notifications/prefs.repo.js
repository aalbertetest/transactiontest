const DEFAULT_PREFS = {
  'task.created': ['console'],
  'task.completed': ['console'],
};

export class UserPrefsRepo {
  constructor(db) {
    this.db = db;
  }

  get(userId) {
    const row = this.db
      .prepare('SELECT prefs_json FROM user_prefs WHERE user_id = ?')
      .get(userId);
    const prefs = row ? JSON.parse(row.prefs_json) : DEFAULT_PREFS;
    return {
      channelsFor(eventName) {
        return prefs[eventName] ?? [];
      },
    };
  }

  set(userId, prefs) {
    this.db
      .prepare(
        `INSERT INTO user_prefs (user_id, prefs_json) VALUES (?, ?)
         ON CONFLICT(user_id) DO UPDATE SET prefs_json = excluded.prefs_json`,
      )
      .run(userId, JSON.stringify(prefs));
  }
}
