import { ConflictException, Injectable, UnauthorizedException } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import * as bcrypt from 'bcryptjs';
import { UsersService } from '../users/users.service';
import { LoginDto } from './dto/login.dto';
import { OAuthCallbackDto } from './dto/oauth-callback.dto';
import { RegisterDto } from './dto/register.dto';

@Injectable()
export class AuthService {
  constructor(
    private readonly usersService: UsersService,
    private readonly jwtService: JwtService,
  ) {}

  private buildAuthResponse(user: { id: string; email: string; name: string }) {
    return {
      user: {
        id: user.id,
        email: user.email,
        name: user.name,
      },
      accessToken: this.jwtService.sign({ sub: user.id, email: user.email }),
    };
  }

  async register(input: RegisterDto) {
    const existing = await this.usersService.findByEmail(input.email);
    if (existing) {
      throw new ConflictException('A user with this email already exists');
    }

    const passwordHash = await bcrypt.hash(input.password, 12);
    const user = await this.usersService.createLocalUser({
      email: input.email,
      name: input.name,
      passwordHash,
    });

    return this.buildAuthResponse(user);
  }

  async login(input: LoginDto) {
    const user = await this.usersService.findByEmail(input.email);
    if (!user?.passwordHash) {
      throw new UnauthorizedException('Invalid credentials');
    }

    const isValid = await bcrypt.compare(input.password, user.passwordHash);
    if (!isValid) {
      throw new UnauthorizedException('Invalid credentials');
    }

    return this.buildAuthResponse(user);
  }

  async oauthCallback(input: OAuthCallbackDto) {
    const user = await this.usersService.findOrCreateOAuthUser({
      provider: input.provider,
      providerUserId: `${input.provider}:${input.code}`,
      email: `${input.code}@${input.provider}.oauth.local`,
      name: `${input.provider}-${input.code}`,
    });

    return this.buildAuthResponse(user);
  }
}
