import { IsString, MinLength } from 'class-validator';

export class CreatePortalDto {
  @IsString()
  @MinLength(3)
  customerId!: string;
}
