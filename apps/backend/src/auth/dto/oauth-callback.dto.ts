import { IsIn, IsString, MinLength } from 'class-validator';

export class OAuthCallbackDto {
  @IsIn(['github', 'google'])
  provider!: 'github' | 'google';

  @IsString()
  @MinLength(4)
  code!: string;
}
