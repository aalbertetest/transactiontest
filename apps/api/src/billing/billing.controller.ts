import { Body, Controller, Get, Headers, Post } from '@nestjs/common';
import { BillingService } from './billing.service';
import { CreateCheckoutDto } from './dto/create-checkout.dto';
import { CreatePortalDto } from './dto/create-portal.dto';

@Controller('billing')
export class BillingController {
  constructor(private readonly billing: BillingService) {}

  @Get('plans')
  plans() {
    return this.billing.getPlans();
  }

  @Post('checkout')
  checkout(@Body() body: CreateCheckoutDto) {
    return this.billing.createCheckoutSession(body.customerId, body.planId);
  }

  @Post('portal')
  portal(@Body() body: CreatePortalDto) {
    return this.billing.createPortalSession(body.customerId);
  }

  @Post('webhook')
  webhook(@Body() body: unknown, @Headers('stripe-signature') signature = '') {
    return this.billing.handleWebhook(body, signature);
  }
}
