import { Body, Controller, Get, Param, Post, Query, UseGuards } from '@nestjs/common';
import { CurrentUser } from './current-user.decorator';
import { AuthService } from './auth.service';
import { LoginDto } from './dto/login.dto';
import { OAuthCallbackDto } from './dto/oauth-callback.dto';
import { RegisterDto } from './dto/register.dto';
import { JwtAuthGuard } from './jwt-auth.guard';

@Controller('auth')
export class AuthController {
  constructor(private readonly authService: AuthService) {}

  @Post('register')
  register(@Body() body: RegisterDto) {
    return this.authService.register(body);
  }

  @Post('login')
  login(@Body() body: LoginDto) {
    return this.authService.login(body);
  }

  @Get('oauth/:provider/start')
  oauthStart(
    @Param('provider') provider: string,
    @Query('redirectUri') redirectUri = 'http://localhost:5173',
  ) {
    return {
      message: 'Mock OAuth start endpoint',
      provider,
      redirectUri,
    };
  }

  @Post('oauth/callback')
  oauthCallback(@Body() body: OAuthCallbackDto) {
    return this.authService.oauthCallback(body);
  }

  @UseGuards(JwtAuthGuard)
  @Get('profile')
  profile(@CurrentUser() user: { sub: string; email: string }) {
    return {
      id: user.sub,
      email: user.email,
    };
  }
}
