import { Module } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { JwtModule } from '@nestjs/jwt';
import type { StringValue } from 'ms';
import { PassportModule } from '@nestjs/passport';
import { UserRepository } from '../users/user.repository';
import { AuthController } from './auth.controller';
import { AuthService } from './auth.service';
import { JwtStrategy } from './jwt.strategy';

@Module({
  imports: [
    PassportModule,
    JwtModule.registerAsync({
      inject: [ConfigService],
      useFactory: (config: ConfigService) => ({
        secret: config.get<string>('JWT_SECRET', 'development-only-secret'),
        signOptions: { expiresIn: config.get<StringValue>('JWT_EXPIRES_IN', '15m') },
      }),
    }),
  ],
  controllers: [AuthController],
  providers: [AuthService, UserRepository, JwtStrategy],
  exports: [AuthService],
})
export class AuthModule {}
