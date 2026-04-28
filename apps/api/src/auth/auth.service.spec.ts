import { JwtService } from '@nestjs/jwt';
import { ConfigService } from '@nestjs/config';
import * as bcrypt from 'bcryptjs';
import { AuthService } from './auth.service';
import { ConflictException, UnauthorizedException } from '@nestjs/common';

describe('AuthService', () => {
  let prisma: any;
  let users: any;
  let jwt: JwtService;
  let config: ConfigService;
  let svc: AuthService;

  beforeEach(() => {
    prisma = {
      refreshToken: {
        create: jest.fn().mockResolvedValue({}),
        findUnique: jest.fn(),
        update: jest.fn().mockResolvedValue({}),
      },
      user: { findUnique: jest.fn(), findFirst: jest.fn(), update: jest.fn() },
    };
    users = {
      findByEmail: jest.fn(),
      create: jest.fn(),
      toPublic: (u: any) => ({ id: u.id, email: u.email, name: u.name, role: u.role, createdAt: new Date().toISOString() }),
    };
    jwt = new JwtService({});
    config = {
      get: (key: string) =>
        ({
          JWT_ACCESS_SECRET: 'access',
          JWT_REFRESH_SECRET: 'refresh',
          JWT_ACCESS_TTL: '60',
          JWT_REFRESH_TTL: '600',
        }[key] ?? ''),
    } as any;
    svc = new AuthService(prisma, users, jwt, config);
  });

  it('rejects duplicate email on register', async () => {
    users.findByEmail.mockResolvedValue({ id: 'u1' });
    await expect(svc.register({ email: 'a@b.co', password: 'password1' })).rejects.toBeInstanceOf(
      ConflictException,
    );
  });

  it('registers a new user and returns tokens', async () => {
    users.findByEmail.mockResolvedValue(null);
    users.create.mockResolvedValue({ id: 'u1', email: 'a@b.co', name: null, role: 'USER' });
    const res = await svc.register({ email: 'a@b.co', password: 'password1' });
    expect(res.accessToken).toBeDefined();
    expect(res.refreshToken).toBeDefined();
    expect(res.user.email).toBe('a@b.co');
    expect(prisma.refreshToken.create).toHaveBeenCalled();
  });

  it('login fails when password is wrong', async () => {
    const hash = await bcrypt.hash('correct', 4);
    users.findByEmail.mockResolvedValue({
      id: 'u1',
      email: 'a@b.co',
      passwordHash: hash,
      role: 'USER',
    });
    await expect(svc.login({ email: 'a@b.co', password: 'wrong' })).rejects.toBeInstanceOf(
      UnauthorizedException,
    );
  });

  it('login succeeds with correct password', async () => {
    const hash = await bcrypt.hash('correct1', 4);
    users.findByEmail.mockResolvedValue({
      id: 'u1',
      email: 'a@b.co',
      passwordHash: hash,
      role: 'USER',
    });
    const res = await svc.login({ email: 'a@b.co', password: 'correct1' });
    expect(res.accessToken).toBeTruthy();
  });
});
