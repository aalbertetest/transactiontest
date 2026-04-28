import { BadRequestException, Injectable, UnauthorizedException } from '@nestjs/common';
import type { BillingInvoice, BillingPlan, BillingSubscription } from '@saas/shared';
import { PrismaService } from '../prisma/prisma.service';
import { BILLING_PLANS } from './billing-plans';
import { MockBillingGateway } from './mock-billing.gateway';

@Injectable()
export class BillingService {
  private readonly gateway = new MockBillingGateway();

  constructor(private readonly prisma: PrismaService) {}

  listPlans(): BillingPlan[] {
    return BILLING_PLANS;
  }

  async createSubscription(userId: string, planCode: string): Promise<BillingSubscription> {
    const plan = BILLING_PLANS.find((entry) => entry.code === planCode);
    if (!plan) {
      throw new BadRequestException('Unknown plan');
    }

    const customer = this.gateway.createCustomer(userId);
    const providerSubscription = this.gateway.createSubscription(customer.id, planCode);
    const providerInvoice = this.gateway.createInvoice(customer.id, plan.amountCents, plan.currency);

    const subscription = await this.prisma.subscription.create({
      data: {
        userId,
        planCode,
        status: 'active',
        providerSubscriptionId: providerSubscription.id,
      },
    });

    await this.prisma.invoice.create({
      data: {
        userId,
        subscriptionId: subscription.id,
        amountCents: providerInvoice.amountCents,
        currency: providerInvoice.currency,
        status: providerInvoice.status,
        providerInvoiceId: providerInvoice.id,
      },
    });

    return {
      id: subscription.id,
      providerSubscriptionId: subscription.providerSubscriptionId,
      planCode: subscription.planCode as BillingSubscription['planCode'],
      status: subscription.status as BillingSubscription['status'],
      startedAt: subscription.startedAt.toISOString(),
      endedAt: subscription.endedAt?.toISOString() ?? null,
    };
  }

  async listInvoices(userId: string): Promise<BillingInvoice[]> {
    const invoices = await this.prisma.invoice.findMany({
      where: { userId },
      orderBy: { issuedAt: 'desc' },
    });

    return invoices.map((invoice) => ({
      id: invoice.id,
      providerInvoiceId: invoice.providerInvoiceId,
      amountCents: invoice.amountCents,
      currency: invoice.currency as BillingInvoice['currency'],
      status: invoice.status as BillingInvoice['status'],
      issuedAt: invoice.issuedAt.toISOString(),
      paidAt: invoice.paidAt?.toISOString() ?? null,
    }));
  }

  async handleWebhook(rawPayload: string, signature: string | undefined, event: Record<string, unknown>) {
    const webhookSecret = process.env.BILLING_WEBHOOK_SECRET ?? 'dev-webhook-secret';

    if (!signature || !this.gateway.verifySignature(rawPayload, signature, webhookSecret)) {
      throw new UnauthorizedException('Invalid webhook signature');
    }

    const created = await this.prisma.billingEvent.create({
      data: {
        eventType: String(event.type ?? 'unknown'),
        payload: JSON.stringify(event),
        signature,
        status: 'processed',
      },
    });

    if (event.type === 'invoice.paid') {
      const invoiceId = String((event.data as Record<string, unknown> | undefined)?.invoiceId ?? '');
      if (invoiceId) {
        await this.prisma.invoice.updateMany({
          where: { id: invoiceId },
          data: {
            status: 'paid',
            paidAt: new Date(),
          },
        });
      }
    }

    return {
      eventId: created.id,
      processed: true,
    };
  }

  buildWebhookSignature(rawPayload: string): string {
    const webhookSecret = process.env.BILLING_WEBHOOK_SECRET ?? 'dev-webhook-secret';
    return this.gateway.signPayload(rawPayload, webhookSecret);
  }
}
