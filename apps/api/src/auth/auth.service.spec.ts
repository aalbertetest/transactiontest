import { UnauthorizedException } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { Test, TestingModule } from '@nestjs/testing';
import { UserRepository } from '../users/user.repository';
import { AuthService } from './auth.service';

describe('AuthService', () => {
  let service: AuthService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        AuthService,
        UserRepository,
        { provide: JwtService, useValue: { signAsync: jest.fn().mockResolvedValue('token') } },
      ],
    }).compile();

    service = module.get(AuthService);
  });

  it('issues a token for valid credentials', async () => {
    await expect(service.login('founder@example.com', 'password')).resolves.toMatchObject({ accessToken: 'token' });
  });

  it('rejects invalid credentials', async () => {
    await expect(service.login('founder@example.com', 'bad-password')).rejects.toBeInstanceOf(UnauthorizedException);
  });
});
