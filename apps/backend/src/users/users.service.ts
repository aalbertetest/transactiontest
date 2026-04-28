import { Injectable } from '@nestjs/common';
import { Prisma, User } from '@prisma/client';
import { PrismaService } from '../prisma/prisma.service';

@Injectable()
export class UsersService {
  constructor(private readonly prisma: PrismaService) {}

  async findByEmail(email: string): Promise<User | null> {
    return this.prisma.user.findUnique({ where: { email } });
  }

  async findById(id: string): Promise<User | null> {
    return this.prisma.user.findUnique({ where: { id } });
  }

  async createLocalUser(input: Prisma.UserCreateInput): Promise<User> {
    return this.prisma.user.create({ data: input });
  }

  async findOrCreateOAuthUser(params: {
    provider: string;
    providerUserId: string;
    email: string;
    name: string;
  }): Promise<User> {
    const existing = await this.prisma.oAuthAccount.findUnique({
      where: {
        provider_providerUserId: {
          provider: params.provider,
          providerUserId: params.providerUserId,
        },
      },
      include: { user: true },
    });

    if (existing) {
      return existing.user;
    }

    const user = await this.prisma.user.upsert({
      where: { email: params.email },
      update: { name: params.name },
      create: {
        email: params.email,
        name: params.name,
      },
    });

    await this.prisma.oAuthAccount.create({
      data: {
        provider: params.provider,
        providerUserId: params.providerUserId,
        userId: user.id,
      },
    });

    return user;
  }
}
