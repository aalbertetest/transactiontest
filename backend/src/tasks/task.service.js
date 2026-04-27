export class NotFoundError extends Error {
  constructor() {
    super('not_found');
    this.code = 'not_found';
  }
}

export class ForbiddenError extends Error {
  constructor() {
    super('forbidden');
    this.code = 'forbidden';
  }
}

export class TaskService {
  constructor({ repo, bus }) {
    this.repo = repo;
    this.bus = bus;
  }

  list(userId, q) {
    return this.repo.listForUser(userId, q);
  }

  async get(userId, id) {
    const task = this.repo.findById(id);
    if (!task) throw new NotFoundError();
    if (task.userId !== userId) throw new ForbiddenError();
    return task;
  }

  async create(userId, input) {
    const task = this.repo.create({ ...input, userId });
    await this.bus.emit('task.created', { task });
    return task;
  }

  async update(userId, id, patch) {
    const before = await this.get(userId, id);
    const after = this.repo.update(id, patch);
    await this.bus.emit('task.updated', { before, after });
    return after;
  }

  async delete(userId, id) {
    const task = await this.get(userId, id);
    this.repo.delete(id);
    await this.bus.emit('task.deleted', { task });
  }
}
