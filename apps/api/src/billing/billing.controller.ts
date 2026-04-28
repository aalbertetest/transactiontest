import {
  Body,
  Controller,
  Get,
  Headers,
  Post,
  Req,
  UseGuards,
} from '@nestjs/common';
import { ApiBearerAuth, ApiTags } from '@nestjs/swagger';
import { IsString } from 'class-validator';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';
import { BillingService } from './billing.service';
import { PaymentProvider } from './payment-provider';

class CheckoutDto {
  @IsString() planId!: string;
}

@ApiTags('billing')
@Controller('billing')
export class BillingController {
  constructor(
    private readonly billing: BillingService,
    private readonly provider: PaymentProvider,
  ) {}

  @Get('plans')
  plans() {
    return this.billing.listPlans();
  }

  @ApiBearerAuth()
  @UseGuards(JwtAuthGuard)
  @Get('subscription')
  subscription(@Req() req: any) {
    return this.billing.getMySubscription(req.user.id);
  }

  @ApiBearerAuth()
  @UseGuards(JwtAuthGuard)
  @Get('invoices')
  invoices(@Req() req: any) {
    return this.billing.listMyInvoices(req.user.id);
  }

  @ApiBearerAuth()
  @UseGuards(JwtAuthGuard)
  @Post('checkout')
  checkout(@Req() req: any, @Body() dto: CheckoutDto) {
    const baseUrl = process.env.WEB_BASE_URL ?? 'http://localhost:5173';
    return this.billing.createCheckout(req.user.id, dto.planId, baseUrl);
  }

  @ApiBearerAuth()
  @UseGuards(JwtAuthGuard)
  @Post('subscribe')
  subscribe(@Req() req: any, @Body() dto: CheckoutDto) {
    return this.billing.subscribeDirectly(req.user.id, dto.planId);
  }

  @ApiBearerAuth()
  @UseGuards(JwtAuthGuard)
  @Post('cancel')
  cancel(@Req() req: any) {
    return this.billing.cancel(req.user.id);
  }

  @Post('webhook')
  webhook(
    @Headers('x-billing-signature') signature: string,
    @Body() body: any,
  ) {
    const secret = process.env.BILLING_WEBHOOK_SECRET ?? 'whsec_test_mock';
    const payload = JSON.stringify(body);
    const event = this.provider.verifyWebhook(payload, signature ?? '', secret);
    return this.billing.handleWebhook(event);
  }
}
