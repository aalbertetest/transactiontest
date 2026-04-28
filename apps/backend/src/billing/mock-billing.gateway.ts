import { createHmac, randomUUID } from 'crypto';

export interface MockCustomer {
  id: string;
  userId: string;
}

export interface MockSubscription {
  id: string;
  customerId: string;
  planCode: string;
}

export interface MockInvoice {
  id: string;
  customerId: string;
  amountCents: number;
  currency: string;
  status: 'open' | 'paid';
}

export class MockBillingGateway {
  createCustomer(userId: string): MockCustomer {
    return {
      id: `cus_${randomUUID().replace(/-/g, '').slice(0, 14)}`,
      userId,
    };
  }

  createSubscription(customerId: string, planCode: string): MockSubscription {
    return {
      id: `sub_${randomUUID().replace(/-/g, '').slice(0, 14)}`,
      customerId,
      planCode,
    };
  }

  createInvoice(customerId: string, amountCents: number, currency: string): MockInvoice {
    return {
      id: `inv_${randomUUID().replace(/-/g, '').slice(0, 14)}`,
      customerId,
      amountCents,
      currency,
      status: 'open',
    };
  }

  signPayload(payload: string, webhookSecret: string): string {
    return createHmac('sha256', webhookSecret).update(payload).digest('hex');
  }

  verifySignature(payload: string, signature: string, webhookSecret: string): boolean {
    const expected = this.signPayload(payload, webhookSecret);
    return expected === signature;
  }
}
