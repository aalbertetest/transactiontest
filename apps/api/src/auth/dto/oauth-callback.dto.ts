import { IsIn, IsString, MinLength } from 'class-validator';

export class OAuthCallbackDto {
  @IsIn(['google', 'github'])
  provider!: string;

  @IsString()
  @MinLength(8)
  code!: string;
}
