import {
  Injectable,
  UnauthorizedException,
  ConflictException,
  BadRequestException,
} from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { ConfigService } from '@nestjs/config';
import * as bcrypt from 'bcryptjs';
import { createHash, randomBytes } from 'crypto';

import { PrismaService } from '../prisma/prisma.service';
import { UsersService } from '../users/users.service';
import { RegisterDto, LoginDto } from './dto';

export interface JwtPayload {
  sub: string;
  email: string;
  role: 'USER' | 'ADMIN';
}

@Injectable()
export class AuthService {
  constructor(
    private readonly prisma: PrismaService,
    private readonly users: UsersService,
    private readonly jwt: JwtService,
    private readonly config: ConfigService,
  ) {}

  async register(dto: RegisterDto) {
    const existing = await this.users.findByEmail(dto.email);
    if (existing) throw new ConflictException('Email already in use');
    const passwordHash = await bcrypt.hash(dto.password, 10);
    const user = await this.users.create({
      email: dto.email,
      name: dto.name ?? null,
      passwordHash,
    });
    const tokens = await this.issueTokens(user.id, user.email, user.role);
    return { user: this.users.toPublic(user), ...tokens };
  }

  async validateUser(email: string, password: string) {
    const user = await this.users.findByEmail(email);
    if (!user || !user.passwordHash) return null;
    const ok = await bcrypt.compare(password, user.passwordHash);
    return ok ? user : null;
  }

  async login(dto: LoginDto) {
    const user = await this.validateUser(dto.email, dto.password);
    if (!user) throw new UnauthorizedException('Invalid credentials');
    const tokens = await this.issueTokens(user.id, user.email, user.role);
    return { user: this.users.toPublic(user), ...tokens };
  }

  async loginOAuthGoogle(profile: {
    email: string;
    name?: string;
    providerId: string;
  }) {
    if (!profile.email) throw new BadRequestException('Email not present in OAuth profile');
    let user = await this.prisma.user.findFirst({
      where: { provider: 'google', providerId: profile.providerId },
    });
    if (!user) {
      const existingByEmail = await this.users.findByEmail(profile.email);
      user = existingByEmail
        ? await this.prisma.user.update({
            where: { id: existingByEmail.id },
            data: { provider: 'google', providerId: profile.providerId },
          })
        : await this.users.create({
            email: profile.email,
            name: profile.name ?? null,
            provider: 'google',
            providerId: profile.providerId,
          });
    }
    return this.issueTokens(user.id, user.email, user.role);
  }

  async refresh(refreshToken: string) {
    const tokenHash = this.hash(refreshToken);
    const stored = await this.prisma.refreshToken.findUnique({ where: { tokenHash } });
    if (!stored || stored.revokedAt || stored.expiresAt < new Date()) {
      throw new UnauthorizedException('Invalid refresh token');
    }
    try {
      this.jwt.verify(refreshToken, {
        secret: this.config.get<string>('JWT_REFRESH_SECRET'),
      });
    } catch {
      throw new UnauthorizedException('Invalid refresh token');
    }
    await this.prisma.refreshToken.update({
      where: { id: stored.id },
      data: { revokedAt: new Date() },
    });
    const user = await this.prisma.user.findUnique({ where: { id: stored.userId } });
    if (!user) throw new UnauthorizedException();
    return this.issueTokens(user.id, user.email, user.role);
  }

  async logout(refreshToken: string) {
    const tokenHash = this.hash(refreshToken);
    await this.prisma.refreshToken
      .update({ where: { tokenHash }, data: { revokedAt: new Date() } })
      .catch(() => undefined);
    return { ok: true };
  }

  private async issueTokens(userId: string, email: string, role: string) {
    const payload: JwtPayload = { sub: userId, email, role: role as 'USER' | 'ADMIN' };
    const accessTtl = Number(this.config.get('JWT_ACCESS_TTL') ?? 900);
    const refreshTtl = Number(this.config.get('JWT_REFRESH_TTL') ?? 60 * 60 * 24 * 30);

    const accessToken = await this.jwt.signAsync(payload, {
      secret: this.config.get<string>('JWT_ACCESS_SECRET'),
      expiresIn: accessTtl,
    });
    const refreshSecret = randomBytes(16).toString('hex');
    const refreshToken = await this.jwt.signAsync(
      { ...payload, jti: refreshSecret },
      {
        secret: this.config.get<string>('JWT_REFRESH_SECRET'),
        expiresIn: refreshTtl,
      },
    );
    await this.prisma.refreshToken.create({
      data: {
        userId,
        tokenHash: this.hash(refreshToken),
        expiresAt: new Date(Date.now() + refreshTtl * 1000),
      },
    });
    return { accessToken, refreshToken };
  }

  private hash(value: string) {
    return createHash('sha256').update(value).digest('hex');
  }
}
