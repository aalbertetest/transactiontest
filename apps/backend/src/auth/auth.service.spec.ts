import { JwtService } from '@nestjs/jwt';
import type { UsersService } from '../users/users.service';
import { AuthService } from './auth.service';

describe('AuthService', () => {
  const usersService = {
    findByEmail: jest.fn(),
    createLocalUser: jest.fn(),
    findOrCreateOAuthUser: jest.fn(),
  } as unknown as UsersService;

  const jwtService = {
    sign: jest.fn().mockReturnValue('signed-token'),
  } as unknown as JwtService;

  const authService = new AuthService(usersService, jwtService);

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('registers and returns access token', async () => {
    (usersService.findByEmail as jest.Mock).mockResolvedValue(null);
    (usersService.createLocalUser as jest.Mock).mockResolvedValue({
      id: 'user_1',
      email: 'alice@example.com',
      name: 'Alice',
    });

    const result = await authService.register({
      name: 'Alice',
      email: 'alice@example.com',
      password: 'Password123!',
    });

    expect(result.accessToken).toBe('signed-token');
    expect(result.user.email).toBe('alice@example.com');
  });

  it('exchanges oauth callback for a token', async () => {
    (usersService.findOrCreateOAuthUser as jest.Mock).mockResolvedValue({
      id: 'oauth_1',
      email: 'abc123@github.oauth.local',
      name: 'github-abc123',
    });

    const result = await authService.oauthCallback({
      provider: 'github',
      code: 'abc123',
    });

    expect(result.user.id).toBe('oauth_1');
    expect(result.accessToken).toBe('signed-token');
  });
});
