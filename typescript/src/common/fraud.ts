import { PaymentIntent } from "./store.js";

export type FraudDecision = "allow" | "review" | "block";

export const evaluateFraud = (intent: PaymentIntent) => {
  let score = 10;
  const signals: Record<string, unknown> = {};

  if (intent.amount > 50000) {
    score += 40;
    signals.high_amount = true;
  }
  if (!["USD", "EUR", "GBP"].includes(intent.currency)) {
    score += 20;
    signals.unsupported_currency = intent.currency;
  }
  if (!intent.customerId) {
    score += 10;
    signals.guest_checkout = true;
  }

  let decision: FraudDecision = "allow";
  if (score >= 60) decision = "block";
  else if (score >= 40) decision = "review";

  return { score, decision, signals };
};
