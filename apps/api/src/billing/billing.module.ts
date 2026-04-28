import { Module } from '@nestjs/common';
import { BillingController } from './billing.controller';
import { BillingService } from './billing.service';
import { PaymentProvider } from './payment-provider';
import { MockStripeProvider } from './providers/mock-stripe.provider';

@Module({
  providers: [
    BillingService,
    { provide: PaymentProvider, useClass: MockStripeProvider },
  ],
  controllers: [BillingController],
  exports: [BillingService],
})
export class BillingModule {}
