package main

import (
	"encoding/json"
	"io"
	"log"
	"net/http"
	"os"
	"strings"
	"time"

	"payment-processing/internal/idempotency"
	"payment-processing/internal/models"
	"payment-processing/internal/store"
	"payment-processing/internal/worker"
)

type paymentIntentCreateRequest struct {
	Amount            int               `json:"amount"`
	Currency          string            `json:"currency"`
	CustomerID        string            `json:"customer_id"`
	PaymentMethodToken string           `json:"payment_method_token"`
	CaptureMethod     string            `json:"capture_method"`
	Metadata          map[string]string `json:"metadata"`
	ReturnURL         string            `json:"return_url"`
}

type paymentIntentResponse struct {
	ID          string `json:"id"`
	Status      string `json:"status"`
	Amount      int    `json:"amount"`
	Currency    string `json:"currency"`
	ClientSecret string `json:"client_secret"`
	ChargeID    string `json:"charge_id,omitempty"`
}

type confirmResponse struct {
	ID       string `json:"id"`
	Status   string `json:"status"`
	ChargeID string `json:"charge_id,omitempty"`
}

type refundRequest struct {
	Amount int    `json:"amount"`
	Reason string `json:"reason"`
}

type refundResponse struct {
	ID       string `json:"id"`
	Status   string `json:"status"`
	Amount   int    `json:"amount"`
	ChargeID string `json:"charge_id"`
}

type webhookEndpointRequest struct {
	URL     string `json:"url"`
	Enabled bool   `json:"enabled"`
}

type webhookEndpointResponse struct {
	ID      string `json:"id"`
	URL     string `json:"url"`
	Enabled bool   `json:"enabled"`
}

func main() {
	apiKey := getenv("API_KEY", "test_key_123")
	if len(store.Store.Merchants) == 0 {
		store.Store.AddMerchant("Demo Merchant", apiKey)
	}

	if getenv("START_WORKER", "false") == "true" {
		go func() {
			w := worker.Worker{
				Store:         store.Store,
				WebhookSecret: getenv("WEBHOOK_SIGNING_SECRET", "whsec_test_123"),
				MaxAttempts:   5,
				BaseBackoff:   200 * time.Millisecond,
				PollInterval:  500 * time.Millisecond,
			}
			w.Run()
		}()
	}

	mux := http.NewServeMux()
	mux.HandleFunc("/v1/payment_intents", handlePaymentIntents)
	mux.HandleFunc("/v1/payment_intents/", handlePaymentIntent)
	mux.HandleFunc("/v1/charges/", handleCharges)
	mux.HandleFunc("/v1/webhook_endpoints", handleWebhookEndpoints)
	mux.HandleFunc("/v1/events", handleEvents)

	addr := getenv("API_ADDR", ":8080")
	log.Printf("listening on %s", addr)
	log.Fatal(http.ListenAndServe(addr, mux))
}

func handlePaymentIntents(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
		return
	}
	merchant, ok := authenticate(w, r)
	if !ok {
		return
	}
	idempotencyKey, ok := requireIdempotencyKey(w, r)
	if !ok {
		return
	}
	body, err := io.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "invalid body", http.StatusBadRequest)
		return
	}
	requestHash := idempotency.HashRequest(r.URL.Path, body)
	if handled := handleIdempotency(w, merchant.ID, idempotencyKey, requestHash); handled {
		return
	}
	var payload paymentIntentCreateRequest
	if err := json.Unmarshal(body, &payload); err != nil {
		http.Error(w, "invalid json", http.StatusBadRequest)
		return
	}
	if payload.Amount <= 0 || payload.Currency == "" || payload.PaymentMethodToken == "" {
		http.Error(w, "invalid request", http.StatusBadRequest)
		return
	}
	intent := store.Store.CreatePaymentIntent(merchant.ID, models.PaymentIntent{
		Amount:            payload.Amount,
		Currency:          strings.ToUpper(payload.Currency),
		CustomerID:        payload.CustomerID,
		PaymentMethodToken: payload.PaymentMethodToken,
		CaptureMethod:     payload.CaptureMethod,
		Metadata:          payload.Metadata,
		ReturnURL:         payload.ReturnURL,
	})
	response := paymentIntentResponse{
		ID:           intent.ID,
		Status:       intent.Status,
		Amount:       intent.Amount,
		Currency:     intent.Currency,
		ClientSecret: intent.ClientSecret,
	}
	writeIdempotentResponse(w, merchant.ID, idempotencyKey, requestHash, response, http.StatusOK)
}

func handlePaymentIntent(w http.ResponseWriter, r *http.Request) {
	merchant, ok := authenticate(w, r)
	if !ok {
		return
	}
	path := strings.TrimPrefix(r.URL.Path, "/v1/payment_intents/")
	segments := strings.Split(path, "/")
	if len(segments) == 0 || segments[0] == "" {
		http.Error(w, "not found", http.StatusNotFound)
		return
	}
	intentID := segments[0]
	if len(segments) == 1 && r.Method == http.MethodGet {
		intent, found := store.Store.GetPaymentIntent(intentID)
		if !found || intent.MerchantID != merchant.ID {
			http.Error(w, "not found", http.StatusNotFound)
			return
		}
		writeJSON(w, paymentIntentResponse{
			ID:           intent.ID,
			Status:       intent.Status,
			Amount:       intent.Amount,
			Currency:     intent.Currency,
			ClientSecret: intent.ClientSecret,
			ChargeID:     intent.ChargeID,
		}, http.StatusOK)
		return
	}
	if len(segments) == 2 && segments[1] == "confirm" && r.Method == http.MethodPost {
		idempotencyKey, ok := requireIdempotencyKey(w, r)
		if !ok {
			return
		}
		requestHash := idempotency.HashRequest(r.URL.Path, []byte(intentID))
		if handled := handleIdempotency(w, merchant.ID, idempotencyKey, requestHash); handled {
			return
		}
		intent, found := store.Store.GetPaymentIntent(intentID)
		if !found || intent.MerchantID != merchant.ID {
			http.Error(w, "not found", http.StatusNotFound)
			return
		}
		if intent.Status != "requires_confirmation" && intent.Status != "processing" {
			writeIdempotentResponse(w, merchant.ID, idempotencyKey, requestHash, confirmResponse{
				ID:       intent.ID,
				Status:   intent.Status,
				ChargeID: intent.ChargeID,
			}, http.StatusOK)
			return
		}
		store.Store.UpdatePaymentIntent(intent.ID, map[string]interface{}{"status": "processing"})
		store.Store.EnqueueTask(models.Task{Type: "process_payment", IntentID: intent.ID})
		writeIdempotentResponse(w, merchant.ID, idempotencyKey, requestHash, confirmResponse{
			ID:     intent.ID,
			Status: "processing",
		}, http.StatusAccepted)
		return
	}
	http.Error(w, "not found", http.StatusNotFound)
}

func handleCharges(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
		return
	}
	merchant, ok := authenticate(w, r)
	if !ok {
		return
	}
	if !strings.HasSuffix(r.URL.Path, "/refunds") {
		http.Error(w, "not found", http.StatusNotFound)
		return
	}
	parts := strings.Split(strings.TrimPrefix(r.URL.Path, "/v1/charges/"), "/")
	if len(parts) < 2 {
		http.Error(w, "not found", http.StatusNotFound)
		return
	}
	chargeID := parts[0]
	idempotencyKey, ok := requireIdempotencyKey(w, r)
	if !ok {
		return
	}
	body, err := io.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "invalid body", http.StatusBadRequest)
		return
	}
	requestHash := idempotency.HashRequest(r.URL.Path, body)
	if handled := handleIdempotency(w, merchant.ID, idempotencyKey, requestHash); handled {
		return
	}
	var payload refundRequest
	if len(body) > 0 {
		if err := json.Unmarshal(body, &payload); err != nil {
			http.Error(w, "invalid json", http.StatusBadRequest)
			return
		}
	}
	charge, found := store.Store.GetCharge(chargeID)
	if !found {
		http.Error(w, "charge not found", http.StatusNotFound)
		return
	}
	refundAmount := payload.Amount
	if refundAmount == 0 {
		refundAmount = charge.Amount
	}
	refund := store.Store.CreateRefund(chargeID, refundAmount, "succeeded")
	store.Store.CreateEvent(merchant.ID, "charge.refunded", map[string]interface{}{
		"id":        refund.ID,
		"charge_id": chargeID,
		"amount":    refund.Amount,
	})
	writeIdempotentResponse(w, merchant.ID, idempotencyKey, requestHash, refundResponse{
		ID:       refund.ID,
		Status:   refund.Status,
		Amount:   refund.Amount,
		ChargeID: chargeID,
	}, http.StatusOK)
}

func handleWebhookEndpoints(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
		return
	}
	merchant, ok := authenticate(w, r)
	if !ok {
		return
	}
	idempotencyKey, ok := requireIdempotencyKey(w, r)
	if !ok {
		return
	}
	body, err := io.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "invalid body", http.StatusBadRequest)
		return
	}
	requestHash := idempotency.HashRequest(r.URL.Path, body)
	if handled := handleIdempotency(w, merchant.ID, idempotencyKey, requestHash); handled {
		return
	}
	var payload webhookEndpointRequest
	if err := json.Unmarshal(body, &payload); err != nil {
		http.Error(w, "invalid json", http.StatusBadRequest)
		return
	}
	endpoint := store.Store.AddWebhookEndpoint(merchant.ID, payload.URL, payload.Enabled)
	writeIdempotentResponse(w, merchant.ID, idempotencyKey, requestHash, webhookEndpointResponse{
		ID:      endpoint.ID,
		URL:     endpoint.URL,
		Enabled: endpoint.Enabled,
	}, http.StatusOK)
}

func handleEvents(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
		return
	}
	merchant, ok := authenticate(w, r)
	if !ok {
		return
	}
	events := store.Store.ListEvents(merchant.ID)
	writeJSON(w, events, http.StatusOK)
}

func authenticate(w http.ResponseWriter, r *http.Request) (models.Merchant, bool) {
	auth := r.Header.Get("Authorization")
	if !strings.HasPrefix(auth, "Bearer ") {
		http.Error(w, "unauthorized", http.StatusUnauthorized)
		return models.Merchant{}, false
	}
	apiKey := strings.TrimSpace(strings.TrimPrefix(auth, "Bearer "))
	merchant, ok := store.Store.GetMerchantByAPIKey(apiKey)
	if !ok {
		http.Error(w, "unauthorized", http.StatusUnauthorized)
		return models.Merchant{}, false
	}
	return merchant, true
}

func requireIdempotencyKey(w http.ResponseWriter, r *http.Request) (string, bool) {
	key := r.Header.Get("Idempotency-Key")
	if key == "" {
		http.Error(w, "missing Idempotency-Key", http.StatusBadRequest)
		return "", false
	}
	return key, true
}

func handleIdempotency(w http.ResponseWriter, merchantID, key, requestHash string) bool {
	if record, ok := store.Store.GetIdempotency(merchantID, key); ok {
		if record.RequestHash != requestHash {
			http.Error(w, "idempotency key reuse with different payload", http.StatusConflict)
			return true
		}
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(record.StatusCode)
		_, _ = w.Write(record.Response)
		return true
	}
	return false
}

func writeIdempotentResponse(w http.ResponseWriter, merchantID, key, requestHash string, payload interface{}, status int) {
	responseBody, _ := json.Marshal(payload)
	store.Store.SetIdempotency(merchantID, key, requestHash, responseBody, status)
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_, _ = w.Write(responseBody)
}

func writeJSON(w http.ResponseWriter, payload interface{}, status int) {
	responseBody, _ := json.Marshal(payload)
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_, _ = w.Write(responseBody)
}

func getenv(key, fallback string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return fallback
}
