package worker

import (
	"time"

	"payment-processing/internal/fraud"
	"payment-processing/internal/processor"
	"payment-processing/internal/retry"
	"payment-processing/internal/store"
	"payment-processing/internal/webhooks"
)

type Worker struct {
	Store          *store.InMemoryStore
	WebhookSecret  string
	MaxAttempts    int
	BaseBackoff    time.Duration
	PollInterval   time.Duration
}

func (w *Worker) Run() {
	for {
		task, ok := w.Store.DequeueTask()
		if !ok {
			time.Sleep(w.PollInterval)
			continue
		}
		switch task.Type {
		case "process_payment":
			w.handleProcessPayment(task.IntentID)
		case "deliver_webhooks":
			w.handleDeliverWebhooks(task.EventID)
		}
	}
}

func (w *Worker) handleProcessPayment(intentID string) {
	intent, ok := w.Store.GetPaymentIntent(intentID)
	if !ok || intent.Status != "processing" {
		return
	}
	score, decision, signals := fraud.Evaluate(intent)
	w.Store.CreateFraudAssessment(intent.ID, score, decision, signals)
	if decision == "block" {
		w.Store.UpdatePaymentIntent(intent.ID, map[string]interface{}{"status": "failed"})
		w.Store.CreateEvent(intent.MerchantID, "payment_intent.failed", map[string]interface{}{
			"id":     intent.ID,
			"status": "failed",
			"reason": "fraud_block",
		})
		return
	}
	client := processor.Client{}
	processorRef, err := retry.WithRetries(
		func() (string, error) {
			return client.Authorize(intent.Amount, intent.Currency, intent.PaymentMethodToken)
		},
		w.MaxAttempts,
		w.BaseBackoff,
		func(err error) bool { return err == processor.ErrRetryable },
	)
	if err != nil {
		reason := "processor_unavailable"
		if err == processor.ErrDeclined {
			reason = "declined"
		}
		w.Store.UpdatePaymentIntent(intent.ID, map[string]interface{}{"status": "failed"})
		w.Store.CreateEvent(intent.MerchantID, "payment_intent.failed", map[string]interface{}{
			"id":     intent.ID,
			"status": "failed",
			"reason": reason,
		})
		return
	}
	charge := w.Store.CreateCharge(intent.ID, intent.Amount, intent.Currency, "succeeded")
	w.Store.UpdatePaymentIntent(intent.ID, map[string]interface{}{
		"status":              "succeeded",
		"charge_id":           charge.ID,
		"processor_reference": processorRef,
	})
	w.Store.CreateEvent(intent.MerchantID, "payment_intent.succeeded", map[string]interface{}{
		"id":        intent.ID,
		"status":    "succeeded",
		"charge_id": charge.ID,
	})
}

func (w *Worker) handleDeliverWebhooks(eventID string) {
	event, ok := w.Store.Events[eventID]
	if !ok {
		return
	}
	endpoints := w.Store.ListWebhookEndpoints(event.MerchantID)
	payload := map[string]interface{}{
		"id":         event.ID,
		"type":       event.Type,
		"created_at": event.CreatedAt,
		"data":       event.Data,
	}
	for _, endpoint := range endpoints {
		_, err := retry.WithRetries(
			func() (string, error) {
				return "ok", webhooks.Deliver(endpoint.URL, w.WebhookSecret, payload)
			},
			w.MaxAttempts,
			w.BaseBackoff,
			func(err error) bool { return true },
		)
		if err != nil {
			w.Store.UpdateEventStatus(event.ID, "failed")
			return
		}
	}
	w.Store.UpdateEventStatus(event.ID, "delivered")
}
