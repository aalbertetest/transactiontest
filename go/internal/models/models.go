package models

type Merchant struct {
	ID     string
	Name   string
	APIKey string
}

type PaymentIntent struct {
	ID                string
	MerchantID        string
	Amount            int
	Currency          string
	CustomerID        string
	PaymentMethodToken string
	CaptureMethod     string
	Metadata          map[string]string
	ReturnURL         string
	Status            string
	ClientSecret      string
	ChargeID          string
	ProcessorReference string
	CreatedAt         string
	UpdatedAt         string
}

type Charge struct {
	ID             string
	PaymentIntentID string
	Amount         int
	Currency       string
	Status         string
	CreatedAt      string
}

type Refund struct {
	ID        string
	ChargeID  string
	Amount    int
	Status    string
	CreatedAt string
}

type WebhookEndpoint struct {
	ID         string
	MerchantID string
	URL        string
	Enabled    bool
	CreatedAt  string
}

type Event struct {
	ID         string
	MerchantID string
	Type       string
	CreatedAt  string
	Data       map[string]interface{}
	Status     string
}

type IdempotencyRecord struct {
	RequestHash string
	Response    []byte
	StatusCode  int
	CreatedAt   string
}

type FraudAssessment struct {
	ID             string
	PaymentIntentID string
	RiskScore      int
	Decision       string
	Signals        map[string]interface{}
	CreatedAt      string
}

type Task struct {
	Type     string
	IntentID string
	EventID  string
}
