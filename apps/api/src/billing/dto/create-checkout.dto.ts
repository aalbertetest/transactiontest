import { IsIn, IsString, MinLength } from 'class-validator';

export class CreateCheckoutDto {
  @IsString()
  @MinLength(3)
  customerId!: string;

  @IsIn(['starter', 'growth', 'scale'])
  planId!: 'starter' | 'growth' | 'scale';
}
