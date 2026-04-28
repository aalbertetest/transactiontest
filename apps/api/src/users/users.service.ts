import { Injectable } from '@nestjs/common';
import { Prisma, User } from '@prisma/client';
import { PrismaService } from '../prisma/prisma.service';
import type { PublicUser } from '@saas/shared';

@Injectable()
export class UsersService {
  constructor(private readonly prisma: PrismaService) {}

  findById(id: string) {
    return this.prisma.user.findUnique({ where: { id } });
  }

  findByEmail(email: string) {
    return this.prisma.user.findUnique({ where: { email } });
  }

  create(data: Prisma.UserCreateInput) {
    return this.prisma.user.create({ data });
  }

  toPublic(u: User): PublicUser {
    return {
      id: u.id,
      email: u.email,
      name: u.name,
      role: u.role as 'USER' | 'ADMIN',
      createdAt: u.createdAt.toISOString(),
    };
  }
}
