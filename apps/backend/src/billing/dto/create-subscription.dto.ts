import { IsIn } from 'class-validator';

export class CreateSubscriptionDto {
  @IsIn(['starter', 'growth', 'enterprise'])
  planCode!: 'starter' | 'growth' | 'enterprise';
}
