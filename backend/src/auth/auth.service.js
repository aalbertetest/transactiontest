import bcrypt from 'bcrypt';
import crypto from 'node:crypto';
import jwt from 'jsonwebtoken';

export class AuthError extends Error {
  constructor(code) {
    super(code);
    this.code = code;
  }
}

// A pre-computed bcrypt hash that no real password will match. Used to keep
// login timing roughly constant even when the user is missing, so an attacker
// can't enumerate accounts via response-time side channels.
const FAKE_HASH =
  '$2b$12$abcdefghijklmnopqrstuuQ8XZ4pPqr3v8jPmYwQ9WqkX0qJ7Yk5oC';

export class AuthService {
  constructor({ users, refreshTokens, config, bus }) {
    this.users = users;
    this.refreshTokens = refreshTokens;
    this.config = config;
    this.bus = bus;
  }

  async register({ email, password }) {
    const existing = this.users.findByEmail(email);
    if (existing) throw new AuthError('email_taken');
    const passwordHash = await bcrypt.hash(password, this.config.bcryptCost);
    const user = this.users.create({ email, passwordHash });
    if (this.bus) await this.bus.emit('user.registered', { user });
    return this._issueTokens(user.id);
  }

  async login({ email, password }) {
    const user = this.users.findByEmail(email);
    const hash = user ? user.passwordHash : FAKE_HASH;
    const ok = await bcrypt.compare(password, hash);
    if (!user || !ok) throw new AuthError('invalid_credentials');
    return this._issueTokens(user.id);
  }

  async refresh(rawToken) {
    const record = this.refreshTokens.findByHash(sha256(rawToken));
    if (!record || record.revokedAt || record.expiresAt < Date.now()) {
      throw new AuthError('invalid_token');
    }
    this.refreshTokens.revoke(record.id);
    return this._issueTokens(record.userId);
  }

  async logout(rawToken) {
    const record = this.refreshTokens.findByHash(sha256(rawToken));
    if (record && !record.revokedAt) this.refreshTokens.revoke(record.id);
  }

  verifyAccessToken(token) {
    try {
      const payload = jwt.verify(token, this.config.jwtSecret, {
        issuer: 'tasks-api',
      });
      return { userId: payload.sub };
    } catch {
      return null;
    }
  }

  async _issueTokens(userId) {
    const accessToken = jwt.sign({ sub: userId }, this.config.jwtSecret, {
      expiresIn: this.config.accessTtl,
      issuer: 'tasks-api',
    });
    const raw = crypto.randomBytes(32).toString('base64url');
    this.refreshTokens.create({
      userId,
      tokenHash: sha256(raw),
      expiresAt: Date.now() + this.config.refreshTtlMs,
    });
    return { accessToken, refreshToken: raw };
  }
}

function sha256(s) {
  return crypto.createHash('sha256').update(s).digest('hex');
}
