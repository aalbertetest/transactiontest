import { Body, Controller, Get, Headers, Post, UseGuards } from '@nestjs/common';
import { CurrentUser } from '../auth/current-user.decorator';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';
import { BillingService } from './billing.service';
import { CreateSubscriptionDto } from './dto/create-subscription.dto';
import { MockWebhookDto } from './dto/mock-webhook.dto';

@Controller('billing')
export class BillingController {
  constructor(private readonly billingService: BillingService) {}

  @Get('plans')
  listPlans() {
    return this.billingService.listPlans();
  }

  @UseGuards(JwtAuthGuard)
  @Post('subscriptions')
  createSubscription(
    @CurrentUser() user: { sub: string },
    @Body() body: CreateSubscriptionDto,
  ) {
    return this.billingService.createSubscription(user.sub, body.planCode);
  }

  @UseGuards(JwtAuthGuard)
  @Get('invoices')
  listInvoices(@CurrentUser() user: { sub: string }) {
    return this.billingService.listInvoices(user.sub);
  }

  @Post('webhooks/mock')
  processMockWebhook(@Body() body: MockWebhookDto, @Headers('x-mock-signature') signature?: string) {
    const rawPayload = JSON.stringify(body);
    return this.billingService.handleWebhook(
      rawPayload,
      signature,
      body as unknown as Record<string, unknown>,
    );
  }
}
