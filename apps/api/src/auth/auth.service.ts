import { Injectable, UnauthorizedException } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { createHash, pbkdf2Sync, timingSafeEqual } from 'node:crypto';
import { UserRecord, UserRepository } from '../users/user.repository';

export interface SessionPayload {
  accessToken: string;
  user: Pick<UserRecord, 'id' | 'email' | 'name'>;
}

@Injectable()
export class AuthService {
  constructor(
    private readonly users: UserRepository,
    private readonly jwt: JwtService,
  ) {}

  async login(email: string, password: string): Promise<SessionPayload> {
    const user = await this.users.findByEmail(email);
    if (!user || !verifyPassword(password, user.passwordHash)) {
      throw new UnauthorizedException('Invalid credentials');
    }
    return this.createSession(user);
  }

  async oauthLogin(provider: string, subject: string): Promise<SessionPayload> {
    const user = await this.users.findByOAuth(provider, subject);
    if (!user) {
      throw new UnauthorizedException('OAuth account is not linked');
    }
    return this.createSession(user);
  }

  private async createSession(user: UserRecord): Promise<SessionPayload> {
    const accessToken = await this.jwt.signAsync({ sub: user.id, email: user.email });
    return { accessToken, user: { id: user.id, email: user.email, name: user.name } };
  }
}

export function hashPassword(password: string, salt = 'demo-salt'): string {
  const digest = pbkdf2Sync(password, salt, 120_000, 32, 'sha256').toString('hex');
  return `pbkdf2_sha256$120000$${salt}$${digest}`;
}

export function verifyPassword(password: string, storedHash: string): boolean {
  const [algorithm, iterations, salt, digest] = storedHash.split('$');
  if (algorithm !== 'pbkdf2_sha256' || !iterations || !salt || !digest) {
    return false;
  }

  const candidate = pbkdf2Sync(password, salt, Number(iterations), 32, 'sha256');
  const expected = Buffer.from(digest, 'hex');
  return candidate.length === expected.length && timingSafeEqual(candidate, expected);
}

export const oauthSubjectForDemo = (token: string) =>
  createHash('sha256').update(token).digest('hex') ===
  createHash('sha256').update('valid-google-demo-code').digest('hex')
    ? 'google-oauth-demo-subject'
    : token;
