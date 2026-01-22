package fraud

import "payment-processing/internal/models"

func Evaluate(intent models.PaymentIntent) (int, string, map[string]interface{}) {
	score := 10
	signals := map[string]interface{}{}
	if intent.Amount > 50000 {
		score += 40
		signals["high_amount"] = true
	}
	if intent.Currency != "USD" && intent.Currency != "EUR" && intent.Currency != "GBP" {
		score += 20
		signals["unsupported_currency"] = intent.Currency
	}
	if intent.CustomerID == "" {
		score += 10
		signals["guest_checkout"] = true
	}
	decision := "allow"
	if score >= 60 {
		decision = "block"
	} else if score >= 40 {
		decision = "review"
	}
	return score, decision, signals
}
