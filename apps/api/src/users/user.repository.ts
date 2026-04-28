import { Injectable } from '@nestjs/common';
import { hashPassword } from '../auth/auth.service';

export interface UserRecord {
  id: string;
  email: string;
  name: string;
  passwordHash: string;
  oauthProvider?: string;
  oauthSubject?: string;
}

@Injectable()
export class UserRepository {
  private readonly users = new Map<string, UserRecord>([
    [
      'founder@example.com',
      {
        id: 'usr_founder',
        email: 'founder@example.com',
        name: 'Demo Founder',
        passwordHash: hashPassword('password'),
        oauthProvider: 'google',
        oauthSubject: 'google-oauth-demo-subject',
      },
    ],
  ]);

  async findByEmail(email: string): Promise<UserRecord | undefined> {
    return this.users.get(email.toLowerCase());
  }

  async findByOAuth(provider: string, subject: string): Promise<UserRecord | undefined> {
    return [...this.users.values()].find(
      (user) => user.oauthProvider === provider && user.oauthSubject === subject,
    );
  }
}
