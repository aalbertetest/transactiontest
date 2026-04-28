import { Module } from '@nestjs/common';
import { BILLING_PROVIDER, BillingService } from './billing.service';
import { BillingController } from './billing.controller';
import { MockStripeBillingProvider } from './mock-stripe.provider';

@Module({
  controllers: [BillingController],
  providers: [
    BillingService,
    MockStripeBillingProvider,
    { provide: BILLING_PROVIDER, useExisting: MockStripeBillingProvider },
  ],
  exports: [BillingService],
})
export class BillingModule {}
