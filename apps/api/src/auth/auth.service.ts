import { Injectable, UnauthorizedException } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { UserRecord, UserRepository } from '../users/user.repository';
import { oauthSubjectForDemo, verifyPassword } from './password';

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

export { oauthSubjectForDemo };
