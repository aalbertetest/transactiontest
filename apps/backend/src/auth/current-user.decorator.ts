import { createParamDecorator, ExecutionContext } from '@nestjs/common';
import type { JwtPayload } from '../common/interfaces/jwt-payload.interface';

export const CurrentUser = createParamDecorator((_: unknown, ctx: ExecutionContext) => {
  const request = ctx.switchToHttp().getRequest<{ user: JwtPayload }>();
  return request.user;
});
