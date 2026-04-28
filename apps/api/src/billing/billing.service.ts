import { Injectable, NotFoundException, BadRequestException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { PaymentProvider, WebhookEvent } from './payment-provider';

@Injectable()
export class BillingService {
  constructor(
    private readonly prisma: PrismaService,
    private readonly provider: PaymentProvider,
  ) {}

  listPlans() {
    return this.prisma.plan.findMany({ where: { active: true }, orderBy: { priceCents: 'asc' } });
  }

  async getMySubscription(userId: string) {
    return this.prisma.subscription.findFirst({
      where: { userId },
      orderBy: { createdAt: 'desc' },
      include: { plan: true },
    });
  }

  async listMyInvoices(userId: string) {
    return this.prisma.invoice.findMany({ where: { userId }, orderBy: { createdAt: 'desc' } });
  }

  async createCheckout(userId: string, planId: string, baseUrl: string) {
    const user = await this.prisma.user.findUnique({ where: { id: userId } });
    if (!user) throw new NotFoundException('User');
    const plan = await this.prisma.plan.findUnique({ where: { id: planId } });
    if (!plan) throw new NotFoundException('Plan');

    const customer = await this.provider.createCustomer({ email: user.email, name: user.name });
    const session = await this.provider.createCheckoutSession({
      customerId: customer.id,
      planId: plan.id,
      priceCents: plan.priceCents,
      successUrl: `${baseUrl}/billing/success`,
      cancelUrl: `${baseUrl}/billing/cancel`,
    });
    return session;
  }

  async subscribeDirectly(userId: string, planId: string) {
    const plan = await this.prisma.plan.findUnique({ where: { id: planId } });
    if (!plan) throw new NotFoundException('Plan');

    const existing = await this.getMySubscription(userId);
    if (existing && existing.status === 'active') {
      throw new BadRequestException('Already subscribed');
    }

    const provSub = await this.provider.createSubscription({
      customerId: `cus_${userId}`,
      planId: plan.id,
    });

    const sub = await this.prisma.subscription.create({
      data: {
        id: provSub.id,
        userId,
        planId: plan.id,
        status: provSub.status,
        currentPeriodEnd: provSub.currentPeriodEnd,
      },
    });

    await this.prisma.invoice.create({
      data: {
        userId,
        subscriptionId: sub.id,
        amountCents: plan.priceCents,
        currency: plan.currency,
        status: 'paid',
      },
    });

    return sub;
  }

  async cancel(userId: string) {
    const sub = await this.getMySubscription(userId);
    if (!sub) throw new NotFoundException('No active subscription');
    await this.provider.cancelSubscription(sub.id);
    return this.prisma.subscription.update({
      where: { id: sub.id },
      data: { cancelAtPeriodEnd: true },
    });
  }

  async handleWebhook(event: WebhookEvent) {
    switch (event.type) {
      case 'checkout.session.completed': {
        const { userId, planId } = event.data ?? {};
        if (userId && planId) await this.subscribeDirectly(userId, planId);
        return { handled: true };
      }
      case 'invoice.paid': {
        const { userId, subscriptionId, amountCents } = event.data ?? {};
        if (userId && subscriptionId) {
          await this.prisma.invoice.create({
            data: {
              userId,
              subscriptionId,
              amountCents: amountCents ?? 0,
              currency: 'usd',
              status: 'paid',
            },
          });
        }
        return { handled: true };
      }
      case 'customer.subscription.deleted': {
        const { subscriptionId } = event.data ?? {};
        if (subscriptionId) {
          await this.prisma.subscription
            .update({ where: { id: subscriptionId }, data: { status: 'canceled' } })
            .catch(() => undefined);
        }
        return { handled: true };
      }
      case 'customer.subscription.updated': {
        const { subscriptionId, status } = event.data ?? {};
        if (subscriptionId && status) {
          await this.prisma.subscription
            .update({ where: { id: subscriptionId }, data: { status } })
            .catch(() => undefined);
        }
        return { handled: true };
      }
      default:
        return { handled: false };
    }
  }
}
