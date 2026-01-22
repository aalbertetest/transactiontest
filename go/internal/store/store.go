package store

import (
	"crypto/rand"
	"encoding/hex"
	"sync"
	"time"

	"payment-processing/internal/models"
)

type InMemoryStore struct {
	mu               sync.Mutex
	Merchants        map[string]models.Merchant
	PaymentIntents   map[string]models.PaymentIntent
	Charges          map[string]models.Charge
	Refunds          map[string]models.Refund
	Idempotency      map[string]models.IdempotencyRecord
	WebhookEndpoints map[string]models.WebhookEndpoint
	Events           map[string]models.Event
	FraudAssessments map[string]models.FraudAssessment
	Tasks            []models.Task
}

func NewInMemoryStore() *InMemoryStore {
	return &InMemoryStore{
		Merchants:        map[string]models.Merchant{},
		PaymentIntents:   map[string]models.PaymentIntent{},
		Charges:          map[string]models.Charge{},
		Refunds:          map[string]models.Refund{},
		Idempotency:      map[string]models.IdempotencyRecord{},
		WebhookEndpoints: map[string]models.WebhookEndpoint{},
		Events:           map[string]models.Event{},
		FraudAssessments: map[string]models.FraudAssessment{},
		Tasks:            []models.Task{},
	}
}

func GenerateID(prefix string) string {
	return prefix + "_" + randomHex(12)
}

func randomHex(bytesLen int) string {
	b := make([]byte, bytesLen)
	_, _ = rand.Read(b)
	return hex.EncodeToString(b)
}

func utcNow() string {
	return time.Now().UTC().Format(time.RFC3339Nano)
}

func (s *InMemoryStore) AddMerchant(name, apiKey string) models.Merchant {
	s.mu.Lock()
	defer s.mu.Unlock()
	merchant := models.Merchant{
		ID:     GenerateID("mch"),
		Name:   name,
		APIKey: apiKey,
	}
	s.Merchants[merchant.ID] = merchant
	return merchant
}

func (s *InMemoryStore) GetMerchantByAPIKey(apiKey string) (models.Merchant, bool) {
	s.mu.Lock()
	defer s.mu.Unlock()
	for _, merchant := range s.Merchants {
		if merchant.APIKey == apiKey {
			return merchant, true
		}
	}
	return models.Merchant{}, false
}

func (s *InMemoryStore) GetIdempotency(merchantID, key string) (models.IdempotencyRecord, bool) {
	record, ok := s.Idempotency[merchantID+":"+key]
	return record, ok
}

func (s *InMemoryStore) SetIdempotency(merchantID, key, requestHash string, response []byte, statusCode int) {
	s.Idempotency[merchantID+":"+key] = models.IdempotencyRecord{
		RequestHash: requestHash,
		Response:    response,
		StatusCode:  statusCode,
		CreatedAt:   utcNow(),
	}
}

func (s *InMemoryStore) CreatePaymentIntent(merchantID string, payload models.PaymentIntent) models.PaymentIntent {
	s.mu.Lock()
	defer s.mu.Unlock()
	intent := payload
	intent.ID = GenerateID("pi")
	intent.MerchantID = merchantID
	intent.Status = "requires_confirmation"
	intent.ClientSecret = intent.ID + "_secret_" + randomHex(8)
	intent.CreatedAt = utcNow()
	intent.UpdatedAt = utcNow()
	s.PaymentIntents[intent.ID] = intent
	return intent
}

func (s *InMemoryStore) GetPaymentIntent(id string) (models.PaymentIntent, bool) {
	intent, ok := s.PaymentIntents[id]
	return intent, ok
}

func (s *InMemoryStore) UpdatePaymentIntent(id string, updates map[string]interface{}) (models.PaymentIntent, bool) {
	s.mu.Lock()
	defer s.mu.Unlock()
	intent, ok := s.PaymentIntents[id]
	if !ok {
		return models.PaymentIntent{}, false
	}
	if status, ok := updates["status"].(string); ok {
		intent.Status = status
	}
	if chargeID, ok := updates["charge_id"].(string); ok {
		intent.ChargeID = chargeID
	}
	if processorRef, ok := updates["processor_reference"].(string); ok {
		intent.ProcessorReference = processorRef
	}
	intent.UpdatedAt = utcNow()
	s.PaymentIntents[id] = intent
	return intent, true
}

func (s *InMemoryStore) CreateCharge(intentID string, amount int, currency, status string) models.Charge {
	s.mu.Lock()
	defer s.mu.Unlock()
	charge := models.Charge{
		ID:              GenerateID("ch"),
		PaymentIntentID: intentID,
		Amount:          amount,
		Currency:        currency,
		Status:          status,
		CreatedAt:       utcNow(),
	}
	s.Charges[charge.ID] = charge
	return charge
}

func (s *InMemoryStore) GetCharge(id string) (models.Charge, bool) {
	charge, ok := s.Charges[id]
	return charge, ok
}

func (s *InMemoryStore) CreateRefund(chargeID string, amount int, status string) models.Refund {
	s.mu.Lock()
	defer s.mu.Unlock()
	refund := models.Refund{
		ID:        GenerateID("rf"),
		ChargeID:  chargeID,
		Amount:    amount,
		Status:    status,
		CreatedAt: utcNow(),
	}
	s.Refunds[refund.ID] = refund
	return refund
}

func (s *InMemoryStore) AddWebhookEndpoint(merchantID, url string, enabled bool) models.WebhookEndpoint {
	s.mu.Lock()
	defer s.mu.Unlock()
	endpoint := models.WebhookEndpoint{
		ID:         GenerateID("we"),
		MerchantID: merchantID,
		URL:        url,
		Enabled:    enabled,
		CreatedAt:  utcNow(),
	}
	s.WebhookEndpoints[endpoint.ID] = endpoint
	return endpoint
}

func (s *InMemoryStore) ListWebhookEndpoints(merchantID string) []models.WebhookEndpoint {
	endpoints := []models.WebhookEndpoint{}
	for _, endpoint := range s.WebhookEndpoints {
		if endpoint.MerchantID == merchantID && endpoint.Enabled {
			endpoints = append(endpoints, endpoint)
		}
	}
	return endpoints
}

func (s *InMemoryStore) CreateEvent(merchantID, eventType string, data map[string]interface{}) models.Event {
	s.mu.Lock()
	defer s.mu.Unlock()
	event := models.Event{
		ID:         GenerateID("evt"),
		MerchantID: merchantID,
		Type:       eventType,
		CreatedAt:  utcNow(),
		Data:       data,
		Status:     "pending",
	}
	s.Events[event.ID] = event
	s.Tasks = append(s.Tasks, models.Task{Type: "deliver_webhooks", EventID: event.ID})
	return event
}

func (s *InMemoryStore) UpdateEventStatus(eventID, status string) {
	s.mu.Lock()
	defer s.mu.Unlock()
	event := s.Events[eventID]
	event.Status = status
	s.Events[eventID] = event
}

func (s *InMemoryStore) ListEvents(merchantID string) []models.Event {
	events := []models.Event{}
	for _, event := range s.Events {
		if event.MerchantID == merchantID {
			events = append(events, event)
		}
	}
	return events
}

func (s *InMemoryStore) CreateFraudAssessment(intentID string, score int, decision string, signals map[string]interface{}) models.FraudAssessment {
	s.mu.Lock()
	defer s.mu.Unlock()
	assessment := models.FraudAssessment{
		ID:             GenerateID("fra"),
		PaymentIntentID: intentID,
		RiskScore:      score,
		Decision:       decision,
		Signals:        signals,
		CreatedAt:      utcNow(),
	}
	s.FraudAssessments[assessment.ID] = assessment
	return assessment
}

func (s *InMemoryStore) EnqueueTask(task models.Task) {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.Tasks = append(s.Tasks, task)
}

func (s *InMemoryStore) DequeueTask() (models.Task, bool) {
	s.mu.Lock()
	defer s.mu.Unlock()
	if len(s.Tasks) == 0 {
		return models.Task{}, false
	}
	task := s.Tasks[0]
	s.Tasks = s.Tasks[1:]
	return task, true
}

var Store = NewInMemoryStore()

