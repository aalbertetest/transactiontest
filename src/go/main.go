package main

import (
	"bytes"
	"crypto/hmac"
	"crypto/sha1"
	"crypto/sha256"
	"encoding/base32"
	"encoding/base64"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"math/rand"
	"net"
	"net/http"
	"os"
	"strconv"
	"strings"
	"sync"
	"time"
)

// ---------------------------
// Configuration and utilities
// ---------------------------

type Config struct {
	GatewayPort       int
	AuthPort          int
	UserPort          int
	PaymentPort       int
	WorkflowPort      int
	QueuePort         int
	StreamPort        int
	CachePort         int
	DBPort            int
	WSPort            int
	SchedulerPort     int
	WorkerPort        int
	JWTSecret         string
	RateLimitPerMin   int
	WorkerConcurrency int
	Env               string
	ServiceOnly       []string
}

func LoadConfig() Config {
	return Config{
		GatewayPort:       getenvInt("GATEWAY_PORT", 8080),
		AuthPort:          getenvInt("AUTH_PORT", 8081),
		UserPort:          getenvInt("USER_PORT", 8082),
		PaymentPort:       getenvInt("PAYMENT_PORT", 8083),
		WorkflowPort:      getenvInt("WORKFLOW_PORT", 8084),
		QueuePort:         getenvInt("QUEUE_PORT", 8085),
		StreamPort:        getenvInt("STREAM_PORT", 8086),
		CachePort:         getenvInt("CACHE_PORT", 8087),
		DBPort:            getenvInt("DB_PORT", 8088),
		WSPort:            getenvInt("WS_PORT", 8089),
		SchedulerPort:     getenvInt("SCHEDULER_PORT", 8090),
		WorkerPort:        getenvInt("WORKER_PORT", 8091),
		JWTSecret:         getenvStr("JWT_SECRET", "dev-secret"),
		RateLimitPerMin:   getenvInt("RATE_LIMIT_PER_MIN", 600),
		WorkerConcurrency: getenvInt("WORKER_CONCURRENCY", 8),
		Env:               getenvStr("ENV", "dev"),
		ServiceOnly:       splitList(getenvStr("SERVICE_ONLY", "")),
	}
}

func getenvInt(key string, def int) int {
	if v := os.Getenv(key); v != "" {
		if i, err := strconv.Atoi(v); err == nil {
			return i
		}
	}
	return def
}

func getenvStr(key, def string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return def
}

func splitList(input string) []string {
	parts := strings.Split(input, ",")
	var out []string
	for _, part := range parts {
		if strings.TrimSpace(part) != "" {
			out = append(out, strings.TrimSpace(part))
		}
	}
	return out
}

func nowUnix() int64 {
	return time.Now().Unix()
}

func newID(prefix string) string {
	return fmt.Sprintf("%s_%d", prefix, rand.Int63())
}

// ---------------------------
// Logging and metrics
// ---------------------------

type Logger struct {
	Service string
}

func (l Logger) Log(level, message string, fields map[string]interface{}) {
	entry := map[string]interface{}{
		"ts":      time.Now().UTC().Format(time.RFC3339Nano),
		"level":   level,
		"service": l.Service,
		"message": message,
		"fields":  fields,
	}
	_ = json.NewEncoder(os.Stdout).Encode(entry)
}

func (l Logger) Info(message string, fields map[string]interface{}) {
	l.Log("INFO", message, fields)
}

func (l Logger) Warn(message string, fields map[string]interface{}) {
	l.Log("WARN", message, fields)
}

func (l Logger) Error(message string, fields map[string]interface{}) {
	l.Log("ERROR", message, fields)
}

type Metrics struct {
	mu        sync.Mutex
	counters  map[string]int
	latencies map[string][]float64
}

func NewMetrics() *Metrics {
	return &Metrics{counters: map[string]int{}, latencies: map[string][]float64{}}
}

func (m *Metrics) Inc(name string, value int) {
	m.mu.Lock()
	defer m.mu.Unlock()
	m.counters[name] += value
}

func (m *Metrics) Observe(name string, value float64) {
	m.mu.Lock()
	defer m.mu.Unlock()
	m.latencies[name] = append(m.latencies[name], value)
}

func (m *Metrics) Render() string {
	m.mu.Lock()
	defer m.mu.Unlock()
	var b strings.Builder
	for name, value := range m.counters {
		b.WriteString(fmt.Sprintf("# TYPE %s counter\n%s %d\n", name, name, value))
	}
	for name, values := range m.latencies {
		var sum float64
		for _, v := range values {
			sum += v
		}
		avg := 0.0
		if len(values) > 0 {
			avg = sum / float64(len(values))
		}
		b.WriteString(fmt.Sprintf("# TYPE %s gauge\n%s_avg %f\n", name, name, avg))
	}
	return b.String()
}

// ---------------------------
// Errors, retry, rate limits
// ---------------------------

type ApiError struct {
	Status    int
	Code      string
	Message   string
	Retryable bool
}

func (e ApiError) Error() string {
	return e.Message
}

// Data models for client/server parity
type User struct {
	ID          string `json:"id"`
	Email       string `json:"email"`
	DisplayName string `json:"display_name"`
	Status      string `json:"status"`
}

type PaymentIntent struct {
	ID             string `json:"id"`
	UserID         string `json:"user_id"`
	Amount         int64  `json:"amount"`
	Currency       string `json:"currency"`
	Status         string `json:"status"`
	IdempotencyKey string `json:"idempotency_key"`
}

type WorkflowRun struct {
	ID          string `json:"id"`
	WorkflowID  string `json:"workflow_id"`
	Status      string `json:"status"`
	CurrentStep string `json:"current_step"`
}

type QueueMessage struct {
	ID      string                 `json:"id"`
	Queue   string                 `json:"queue"`
	Payload map[string]interface{} `json:"payload"`
	Attempt int                    `json:"attempt"`
}

type StreamRecord struct {
	Topic     string `json:"topic"`
	Partition int    `json:"partition"`
	Offset    int64  `json:"offset"`
	Key       string `json:"key"`
	Value     string `json:"value"`
}

func withRetry(fn func() error, retries int) error {
	var last error
	for i := 0; i <= retries; i++ {
		if err := fn(); err != nil {
			last = err
			time.Sleep(time.Duration(50*(1<<i)) * time.Millisecond)
			continue
		}
		return nil
	}
	return last
}

type RateLimiter struct {
	mu     sync.Mutex
	limit  int
	tokens map[string]int
	ts     map[string]int64
}

func NewRateLimiter(limit int) *RateLimiter {
	return &RateLimiter{limit: limit, tokens: map[string]int{}, ts: map[string]int64{}}
}

func (r *RateLimiter) Allow(key string) bool {
	r.mu.Lock()
	defer r.mu.Unlock()
	now := nowUnix()
	last, ok := r.ts[key]
	if !ok || now-last >= 60 {
		r.tokens[key] = r.limit
		r.ts[key] = now
	}
	if r.tokens[key] <= 0 {
		return false
	}
	r.tokens[key]--
	return true
}

type IdempotencyStore struct {
	mu    sync.Mutex
	ttl   int64
	store map[string]struct {
		ts    int64
		value map[string]interface{}
	}
}

func NewIdempotencyStore() *IdempotencyStore {
	return &IdempotencyStore{ttl: 3600, store: map[string]struct {
		ts    int64
		value map[string]interface{}
	}{}}
}

func (s *IdempotencyStore) Get(key string) map[string]interface{} {
	s.mu.Lock()
	defer s.mu.Unlock()
	entry, ok := s.store[key]
	if !ok {
		return nil
	}
	if nowUnix()-entry.ts > s.ttl {
		delete(s.store, key)
		return nil
	}
	return entry.value
}

func (s *IdempotencyStore) Set(key string, value map[string]interface{}) {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.store[key] = struct {
		ts    int64
		value map[string]interface{}
	}{ts: nowUnix(), value: value}
}

// ---------------------------
// HTTP routing and middleware
// ---------------------------

type Context struct {
	W              http.ResponseWriter
	R              *http.Request
	Body           map[string]interface{}
	Params         map[string]string
	CorrelationID  string
	IdempotencyKey string
	Config         *Config
}

type HandlerFunc func(ctx *Context) error
type Middleware func(next HandlerFunc) HandlerFunc

type Route struct {
	Method     string
	Segments   []string
	Handler    HandlerFunc
	Middleware []Middleware
}

type Router struct {
	Routes []Route
}

func (r *Router) Add(method, path string, handler HandlerFunc, middleware ...Middleware) {
	segments := strings.Split(strings.Trim(path, "/"), "/")
	r.Routes = append(r.Routes, Route{
		Method:     strings.ToUpper(method),
		Segments:   segments,
		Handler:    handler,
		Middleware: middleware,
	})
}

func (r *Router) ServeHTTP(w http.ResponseWriter, req *http.Request) {
	path := strings.Split(req.URL.Path, "?")[0]
	segments := strings.Split(strings.Trim(path, "/"), "/")
	for _, route := range r.Routes {
		if route.Method != req.Method {
			continue
		}
		if len(route.Segments) != len(segments) {
			continue
		}
		params := map[string]string{}
		matched := true
		for i, seg := range route.Segments {
			if strings.HasPrefix(seg, "{") && strings.HasSuffix(seg, "}") {
				params[strings.Trim(seg, "{}")] = segments[i]
			} else if seg != segments[i] {
				matched = false
				break
			}
		}
		if !matched {
			continue
		}
		body := map[string]interface{}{}
		if req.Body != nil {
			_ = json.NewDecoder(req.Body).Decode(&body)
		}
		ctx := &Context{
			W:              w,
			R:              req,
			Body:           body,
			Params:         params,
			CorrelationID:  req.Header.Get("Correlation-Id"),
			IdempotencyKey: req.Header.Get("Idempotency-Key"),
		}
		handler := route.Handler
		for i := len(route.Middleware) - 1; i >= 0; i-- {
			handler = route.Middleware[i](handler)
		}
		if err := handler(ctx); err != nil {
			if apiErr, ok := err.(ApiError); ok {
				JSON(ctx.W, apiErr.Status, map[string]interface{}{
					"error": map[string]interface{}{
						"code":       apiErr.Code,
						"message":    apiErr.Message,
						"retryable":  apiErr.Retryable,
						"request_id": ctx.CorrelationID,
					},
				})
				return
			}
			JSON(ctx.W, http.StatusInternalServerError, map[string]interface{}{
				"error": map[string]interface{}{
					"code":    "internal_error",
					"message": "internal error",
				},
			})
			return
		}
		return
	}
	JSON(w, http.StatusNotFound, map[string]interface{}{
		"error": map[string]interface{}{
			"code":    "not_found",
			"message": "route not found",
		},
	})
}

func JSON(w http.ResponseWriter, status int, body interface{}) {
	data, _ := json.Marshal(body)
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_, _ = w.Write(data)
}

func middlewareLogging(logger Logger, metrics *Metrics) Middleware {
	return func(next HandlerFunc) HandlerFunc {
		return func(ctx *Context) error {
			start := time.Now()
			logger.Info("request_start", map[string]interface{}{"path": ctx.R.URL.Path})
			err := next(ctx)
			metrics.Inc("http_requests_total", 1)
			metrics.Observe("http_request_latency_seconds", time.Since(start).Seconds())
			return err
		}
	}
}

func middlewareRateLimit(limiter *RateLimiter) Middleware {
	return func(next HandlerFunc) HandlerFunc {
		return func(ctx *Context) error {
			ip := strings.Split(ctx.R.RemoteAddr, ":")[0]
			if !limiter.Allow(ip) {
				return ApiError{Status: http.StatusTooManyRequests, Code: "rate_limited", Message: "Too many requests", Retryable: true}
			}
			return next(ctx)
		}
	}
}

func middlewareAuth(secret string) Middleware {
	return func(next HandlerFunc) HandlerFunc {
		return func(ctx *Context) error {
			auth := ctx.R.Header.Get("Authorization")
			token := strings.TrimPrefix(auth, "Bearer ")
			if token == "" {
				return ApiError{Status: http.StatusUnauthorized, Code: "missing_token", Message: "Missing token"}
			}
			if _, err := jwtDecode(token, secret); err != nil {
				return err
			}
			return next(ctx)
		}
	}
}

// ---------------------------
// Stores and brokers
// ---------------------------

type CacheStore struct {
	mu    sync.Mutex
	items map[string]struct {
		Value string
		Exp   int64
	}
}

func NewCacheStore() *CacheStore {
	return &CacheStore{items: map[string]struct {
		Value string
		Exp   int64
	}{}}
}

func (c *CacheStore) Get(key string) (string, bool) {
	c.mu.Lock()
	defer c.mu.Unlock()
	entry, ok := c.items[key]
	if !ok {
		return "", false
	}
	if entry.Exp > 0 && nowUnix() > entry.Exp {
		delete(c.items, key)
		return "", false
	}
	return entry.Value, true
}

func (c *CacheStore) Put(key, value string, ttl int64) {
	c.mu.Lock()
	defer c.mu.Unlock()
	exp := int64(0)
	if ttl > 0 {
		exp = nowUnix() + ttl
	}
	c.items[key] = struct {
		Value string
		Exp   int64
	}{Value: value, Exp: exp}
}

func (c *CacheStore) Delete(key string) {
	c.mu.Lock()
	defer c.mu.Unlock()
	delete(c.items, key)
}

type QueueBroker struct {
	mu       sync.Mutex
	queues   map[string][]map[string]interface{}
	inflight map[string]map[string]interface{}
}

func NewQueueBroker() *QueueBroker {
	return &QueueBroker{queues: map[string][]map[string]interface{}{}, inflight: map[string]map[string]interface{}{}}
}

func (q *QueueBroker) Enqueue(name string, payload map[string]interface{}) map[string]interface{} {
	msg := map[string]interface{}{
		"id":         newID("msg"),
		"queue":      name,
		"payload":    payload,
		"attempt":    0,
		"visible_at": nowUnix(),
	}
	q.mu.Lock()
	defer q.mu.Unlock()
	q.queues[name] = append(q.queues[name], msg)
	return msg
}

func (q *QueueBroker) Dequeue(name string, max int) []map[string]interface{} {
	now := nowUnix()
	q.mu.Lock()
	defer q.mu.Unlock()
	queue := q.queues[name]
	var msgs []map[string]interface{}
	for _, msg := range queue {
		if len(msgs) >= max {
			break
		}
		if v, ok := msg["visible_at"].(int64); ok && v <= now {
			msg["attempt"] = msg["attempt"].(int) + 1
			msg["visible_at"] = now + 30
			q.inflight[msg["id"].(string)] = msg
			msgs = append(msgs, msg)
		}
	}
	return msgs
}

func (q *QueueBroker) Ack(messageID string, success bool) {
	q.mu.Lock()
	defer q.mu.Unlock()
	msg, ok := q.inflight[messageID]
	if !ok {
		return
	}
	delete(q.inflight, messageID)
	if !success {
		attempt := msg["attempt"].(int)
		msg["visible_at"] = nowUnix() + int64(60*attempt)
		queue := msg["queue"].(string)
		q.queues[queue] = append(q.queues[queue], msg)
	}
}

type StreamBroker struct {
	mu      sync.Mutex
	topics  map[string]map[string]interface{}
	offsets map[string]map[string]int64
}

func NewStreamBroker() *StreamBroker {
	return &StreamBroker{topics: map[string]map[string]interface{}{}, offsets: map[string]map[string]int64{}}
}

func (s *StreamBroker) CreateTopic(name string, partitions int) {
	if partitions <= 0 {
		partitions = 3
	}
	if _, ok := s.topics[name]; ok {
		return
	}
	records := map[int][]map[string]interface{}{}
	offsets := map[int]int64{}
	for i := 0; i < partitions; i++ {
		records[i] = []map[string]interface{}{}
		offsets[i] = 0
	}
	s.topics[name] = map[string]interface{}{
		"partitions": partitions,
		"records":    records,
		"offsets":    offsets,
	}
}

func (s *StreamBroker) Publish(topic, key, value string) map[string]interface{} {
	s.mu.Lock()
	defer s.mu.Unlock()
	if _, ok := s.topics[topic]; !ok {
		s.CreateTopic(topic, 3)
	}
	info := s.topics[topic]
	partitions := info["partitions"].(int)
	partition := int(hashString(key)) % partitions
	offsets := info["offsets"].(map[int]int64)
	offset := offsets[partition]
	record := map[string]interface{}{
		"topic":     topic,
		"partition": partition,
		"offset":    offset,
		"key":       key,
		"value":     value,
	}
	records := info["records"].(map[int][]map[string]interface{})
	records[partition] = append(records[partition], record)
	offsets[partition] = offset + 1
	return record
}

func (s *StreamBroker) Consume(topic, group string, max int) []map[string]interface{} {
	s.mu.Lock()
	defer s.mu.Unlock()
	info, ok := s.topics[topic]
	if !ok {
		return nil
	}
	partitions := info["partitions"].(int)
	if s.offsets[group] == nil {
		s.offsets[group] = map[string]int64{}
	}
	var out []map[string]interface{}
	records := info["records"].(map[int][]map[string]interface{})
	for p := 0; p < partitions; p++ {
		key := fmt.Sprintf("%s:%d", topic, p)
		offset := s.offsets[group][key]
		for _, rec := range records[p] {
			if rec["offset"].(int64) >= offset {
				out = append(out, rec)
				if len(out) >= max {
					return out
				}
			}
		}
	}
	return out
}

func (s *StreamBroker) Commit(topic, group string, partition int, offset int64) {
	s.mu.Lock()
	defer s.mu.Unlock()
	if s.offsets[group] == nil {
		s.offsets[group] = map[string]int64{}
	}
	key := fmt.Sprintf("%s:%d", topic, partition)
	s.offsets[group][key] = offset
}

func hashString(s string) uint32 {
	sum := sha256.Sum256([]byte(s))
	return uint32(sum[0])<<24 | uint32(sum[1])<<16 | uint32(sum[2])<<8 | uint32(sum[3])
}

type DocumentStore struct {
	mu    sync.Mutex
	items map[string]map[string]map[string]interface{}
}

func NewDocumentStore() *DocumentStore {
	return &DocumentStore{items: map[string]map[string]map[string]interface{}{}}
}

func (d *DocumentStore) Get(collection, key string) (map[string]interface{}, bool) {
	d.mu.Lock()
	defer d.mu.Unlock()
	col := d.items[collection]
	if col == nil {
		return nil, false
	}
	val, ok := col[key]
	return val, ok
}

func (d *DocumentStore) Put(collection, key string, doc map[string]interface{}) {
	d.mu.Lock()
	defer d.mu.Unlock()
	if d.items[collection] == nil {
		d.items[collection] = map[string]map[string]interface{}{}
	}
	d.items[collection][key] = doc
}

// ---------------------------
// WebSocket hub
// ---------------------------

type WSConnection struct {
	conn net.Conn
	mu   sync.Mutex
}

func (c *WSConnection) SendText(payload string) error {
	c.mu.Lock()
	defer c.mu.Unlock()
	data := []byte(payload)
	header := []byte{0x81, byte(len(data))}
	_, err := c.conn.Write(append(header, data...))
	return err
}

type WebSocketHub struct {
	mu    sync.Mutex
	conns []*WSConnection
}

func NewWebSocketHub() *WebSocketHub {
	return &WebSocketHub{}
}

func (h *WebSocketHub) Register(conn *WSConnection) {
	h.mu.Lock()
	defer h.mu.Unlock()
	h.conns = append(h.conns, conn)
}

func (h *WebSocketHub) Publish(payload string) {
	h.mu.Lock()
	conns := append([]*WSConnection{}, h.conns...)
	h.mu.Unlock()
	for _, conn := range conns {
		_ = conn.SendText(payload)
	}
}

// ---------------------------
// JWT and MFA helpers
// ---------------------------

func jwtEncode(payload map[string]interface{}, secret string, expiresIn int64) (string, error) {
	header := map[string]string{"alg": "HS256", "typ": "JWT"}
	payload["exp"] = nowUnix() + expiresIn
	hb, _ := json.Marshal(header)
	pb, _ := json.Marshal(payload)
	headerB64 := base64.RawURLEncoding.EncodeToString(hb)
	payloadB64 := base64.RawURLEncoding.EncodeToString(pb)
	signing := headerB64 + "." + payloadB64
	mac := hmac.New(sha256.New, []byte(secret))
	mac.Write([]byte(signing))
	sig := base64.RawURLEncoding.EncodeToString(mac.Sum(nil))
	return signing + "." + sig, nil
}

func jwtDecode(token, secret string) (map[string]interface{}, error) {
	parts := strings.Split(token, ".")
	if len(parts) != 3 {
		return nil, ApiError{Status: http.StatusUnauthorized, Code: "invalid_token", Message: "Invalid token"}
	}
	signing := parts[0] + "." + parts[1]
	mac := hmac.New(sha256.New, []byte(secret))
	mac.Write([]byte(signing))
	expected := mac.Sum(nil)
	actual, _ := base64.RawURLEncoding.DecodeString(parts[2])
	if !hmac.Equal(expected, actual) {
		return nil, ApiError{Status: http.StatusUnauthorized, Code: "invalid_token", Message: "Signature mismatch"}
	}
	payloadBytes, _ := base64.RawURLEncoding.DecodeString(parts[1])
	payload := map[string]interface{}{}
	_ = json.Unmarshal(payloadBytes, &payload)
	exp, _ := payload["exp"].(float64)
	if int64(exp) < nowUnix() {
		return nil, ApiError{Status: http.StatusUnauthorized, Code: "expired_token", Message: "Token expired"}
	}
	return payload, nil
}

func totp(secret string, timestamp int64) (string, error) {
	if timestamp == 0 {
		timestamp = nowUnix()
	}
	counter := timestamp / 30
	key, err := base32.StdEncoding.DecodeString(strings.ToUpper(secret))
	if err != nil {
		return "", err
	}
	msg := make([]byte, 8)
	for i := 7; i >= 0; i-- {
		msg[i] = byte(counter & 0xff)
		counter >>= 8
	}
	mac := hmac.New(sha1.New, key)
	mac.Write(msg)
	digest := mac.Sum(nil)
	offset := digest[len(digest)-1] & 0x0f
	code := (int(digest[offset])&0x7f)<<24 | int(digest[offset+1])<<16 | int(digest[offset+2])<<8 | int(digest[offset+3])
	return fmt.Sprintf("%06d", code%1000000), nil
}

// ---------------------------
// Services
// ---------------------------

type AuthService struct {
	config        Config
	clients       map[string]string
	authCodes     map[string]string
	refreshTokens map[string]string
	mfa           map[string]string
}

func NewAuthService(cfg Config) *AuthService {
	return &AuthService{
		config:        cfg,
		clients:       map[string]string{},
		authCodes:     map[string]string{},
		refreshTokens: map[string]string{},
		mfa:           map[string]string{},
	}
}

func (a *AuthService) RegisterClient(id, secret string) {
	a.clients[id] = secret
}

func (a *AuthService) Authorize(ctx *Context) error {
	clientID := getStr(ctx.Body, "client_id")
	userID := getStr(ctx.Body, "user_id")
	if clientID == "" || userID == "" {
		return ApiError{Status: http.StatusUnauthorized, Code: "invalid_client", Message: "Invalid client"}
	}
	code := newID("code")
	a.authCodes[code] = userID
	JSON(ctx.W, http.StatusOK, map[string]interface{}{"code": code, "state": ctx.Body["state"]})
	return nil
}

func (a *AuthService) Token(ctx *Context) error {
	grantType := getStr(ctx.Body, "grant_type")
	if grantType == "" {
		grantType = "authorization_code"
	}
	if grantType == "authorization_code" {
		code := getStr(ctx.Body, "code")
		clientID := getStr(ctx.Body, "client_id")
		clientSecret := getStr(ctx.Body, "client_secret")
		if a.clients[clientID] != clientSecret {
			return ApiError{Status: http.StatusUnauthorized, Code: "invalid_client", Message: "Invalid client"}
		}
		userID := a.authCodes[code]
		if userID == "" {
			return ApiError{Status: http.StatusUnauthorized, Code: "invalid_code", Message: "Invalid code"}
		}
		token, _ := jwtEncode(map[string]interface{}{"sub": userID, "scope": "basic", "mfa": false}, a.config.JWTSecret, 3600)
		refresh := newID("rft")
		a.refreshTokens[refresh] = userID
		JSON(ctx.W, http.StatusOK, map[string]interface{}{"access_token": token, "refresh_token": refresh, "expires_in": 3600})
		return nil
	}
	return ApiError{Status: http.StatusBadRequest, Code: "unsupported_grant", Message: "Unsupported grant"}
}

func (a *AuthService) Refresh(ctx *Context) error {
	token := getStr(ctx.Body, "refresh_token")
	userID := a.refreshTokens[token]
	if userID == "" {
		return ApiError{Status: http.StatusUnauthorized, Code: "invalid_refresh", Message: "Invalid refresh token"}
	}
	access, _ := jwtEncode(map[string]interface{}{"sub": userID, "scope": "basic", "mfa": true}, a.config.JWTSecret, 3600)
	JSON(ctx.W, http.StatusOK, map[string]interface{}{"access_token": access, "refresh_token": token, "expires_in": 3600})
	return nil
}

func (a *AuthService) EnrollMfa(ctx *Context) error {
	userID := getStr(ctx.Body, "user_id")
	if userID == "" {
		return ApiError{Status: http.StatusBadRequest, Code: "missing_user", Message: "user_id required"}
	}
	secret := base32.StdEncoding.EncodeToString([]byte(newID("mfa")))
	a.mfa[userID] = secret
	uri := fmt.Sprintf("otpauth://totp/Platform:%s?secret=%s&issuer=Platform", userID, secret)
	JSON(ctx.W, http.StatusOK, map[string]interface{}{"secret": secret, "uri": uri})
	return nil
}

func (a *AuthService) VerifyMfa(ctx *Context) error {
	userID := getStr(ctx.Body, "user_id")
	code := getStr(ctx.Body, "code")
	secret := a.mfa[userID]
	if secret == "" {
		return ApiError{Status: http.StatusNotFound, Code: "mfa_not_enrolled", Message: "MFA not enrolled"}
	}
	expected, _ := totp(secret, 0)
	JSON(ctx.W, http.StatusOK, map[string]interface{}{"verified": expected == code})
	return nil
}

type UserService struct {
	mu    sync.Mutex
	users map[string]map[string]interface{}
}

func NewUserService() *UserService {
	return &UserService{users: map[string]map[string]interface{}{}}
}

func (u *UserService) Register(ctx *Context) error {
	email := getStr(ctx.Body, "email")
	displayName := getStr(ctx.Body, "display_name")
	if email == "" || !strings.Contains(email, "@") || displayName == "" {
		return ApiError{Status: http.StatusBadRequest, Code: "invalid_user", Message: "Invalid user data"}
	}
	id := newID("usr")
	u.mu.Lock()
	u.users[id] = map[string]interface{}{"id": id, "email": email, "display_name": displayName, "status": "active"}
	u.mu.Unlock()
	JSON(ctx.W, http.StatusCreated, u.users[id])
	return nil
}

func (u *UserService) Get(ctx *Context) error {
	id := ctx.Params["id"]
	u.mu.Lock()
	user := u.users[id]
	u.mu.Unlock()
	if user == nil {
		return ApiError{Status: http.StatusNotFound, Code: "not_found", Message: "User not found"}
	}
	JSON(ctx.W, http.StatusOK, user)
	return nil
}

func (u *UserService) Update(ctx *Context) error {
	id := ctx.Params["id"]
	u.mu.Lock()
	user := u.users[id]
	if user == nil {
		u.mu.Unlock()
		return ApiError{Status: http.StatusNotFound, Code: "not_found", Message: "User not found"}
	}
	if v := getStr(ctx.Body, "display_name"); v != "" {
		user["display_name"] = v
	}
	if v := getStr(ctx.Body, "status"); v != "" {
		user["status"] = v
	}
	u.mu.Unlock()
	JSON(ctx.W, http.StatusOK, user)
	return nil
}

type PaymentService struct {
	mu         sync.Mutex
	intents    map[string]map[string]interface{}
	queue      *QueueBroker
	stream     *StreamBroker
	idempotent *IdempotencyStore
}

func NewPaymentService(queue *QueueBroker, stream *StreamBroker, idem *IdempotencyStore) *PaymentService {
	return &PaymentService{intents: map[string]map[string]interface{}{}, queue: queue, stream: stream, idempotent: idem}
}

func (p *PaymentService) CreateIntent(ctx *Context) error {
	key := ctx.IdempotencyKey
	if key == "" {
		key = getStr(ctx.Body, "idempotency_key")
	}
	if key == "" {
		return ApiError{Status: http.StatusBadRequest, Code: "missing_idempotency", Message: "Idempotency-Key required"}
	}
	if cached := p.idempotent.Get(key); cached != nil {
		JSON(ctx.W, http.StatusOK, cached)
		return nil
	}
	id := newID("pi")
	intent := map[string]interface{}{
		"id":     id,
		"user":   ctx.Body["user_id"],
		"amount": ctx.Body["amount"],
		"currency": ctx.Body["currency"],
		"status": "pending",
	}
	p.mu.Lock()
	p.intents[id] = intent
	p.mu.Unlock()
	p.queue.Enqueue("payments", map[string]interface{}{"intent_id": id})
	p.idempotent.Set(key, map[string]interface{}{"id": id, "status": "pending"})
	JSON(ctx.W, http.StatusAccepted, map[string]interface{}{"id": id, "status": "pending"})
	return nil
}

func (p *PaymentService) GetIntent(ctx *Context) error {
	id := ctx.Params["id"]
	p.mu.Lock()
	intent := p.intents[id]
	p.mu.Unlock()
	if intent == nil {
		return ApiError{Status: http.StatusNotFound, Code: "not_found", Message: "Payment intent not found"}
	}
	JSON(ctx.W, http.StatusOK, intent)
	return nil
}

func (p *PaymentService) CaptureIntent(ctx *Context) error {
	id := ctx.Params["id"]
	p.mu.Lock()
	intent := p.intents[id]
	if intent == nil {
		p.mu.Unlock()
		return ApiError{Status: http.StatusNotFound, Code: "not_found", Message: "Payment intent not found"}
	}
	intent["status"] = "captured"
	p.mu.Unlock()
	JSON(ctx.W, http.StatusOK, intent)
	return nil
}

func (p *PaymentService) RefundIntent(ctx *Context) error {
	id := ctx.Params["id"]
	p.mu.Lock()
	intent := p.intents[id]
	if intent == nil {
		p.mu.Unlock()
		return ApiError{Status: http.StatusNotFound, Code: "not_found", Message: "Payment intent not found"}
	}
	intent["status"] = "refunded"
	p.mu.Unlock()
	JSON(ctx.W, http.StatusOK, intent)
	return nil
}

func (p *PaymentService) ProcessCharge(payload map[string]interface{}) {
	id, _ := payload["intent_id"].(string)
	p.mu.Lock()
	intent := p.intents[id]
	if intent != nil {
		intent["status"] = "succeeded"
	}
	p.mu.Unlock()
	p.stream.Publish("payments", id, `{"status":"succeeded"}`)
}

type WorkflowEngine struct {
	mu      sync.Mutex
	flows   map[string]map[string]interface{}
	runs    map[string]map[string]interface{}
	queue   *QueueBroker
	stream  *StreamBroker
}

func NewWorkflowEngine(queue *QueueBroker, stream *StreamBroker) *WorkflowEngine {
	return &WorkflowEngine{flows: map[string]map[string]interface{}{}, runs: map[string]map[string]interface{}{}, queue: queue, stream: stream}
}

func (w *WorkflowEngine) Register(ctx *Context) error {
	id := newID("wf")
	w.mu.Lock()
	w.flows[id] = map[string]interface{}{"id": id, "name": ctx.Body["name"], "definition": ctx.Body["definition"]}
	w.mu.Unlock()
	JSON(ctx.W, http.StatusCreated, map[string]interface{}{"workflow_id": id})
	return nil
}

func (w *WorkflowEngine) Start(ctx *Context) error {
	id := ctx.Params["id"]
	runID := newID("wr")
	w.mu.Lock()
	w.runs[runID] = map[string]interface{}{"id": runID, "workflow_id": id, "status": "running", "current_step": "start"}
	w.mu.Unlock()
	w.queue.Enqueue("workflow", map[string]interface{}{"run_id": runID, "step": "start"})
	w.stream.Publish("workflows", runID, `{"status":"running"}`)
	JSON(ctx.W, http.StatusAccepted, map[string]interface{}{"run_id": runID, "status": "running"})
	return nil
}

func (w *WorkflowEngine) GetRun(ctx *Context) error {
	runID := ctx.Params["run_id"]
	w.mu.Lock()
	run := w.runs[runID]
	w.mu.Unlock()
	if run == nil {
		return ApiError{Status: http.StatusNotFound, Code: "not_found", Message: "Workflow run not found"}
	}
	JSON(ctx.W, http.StatusOK, run)
	return nil
}

func (w *WorkflowEngine) ProcessTask(payload map[string]interface{}) {
	runID, _ := payload["run_id"].(string)
	step, _ := payload["step"].(string)
	w.mu.Lock()
	run := w.runs[runID]
	if run != nil {
		run["current_step"] = step
		if step == "complete" {
			run["status"] = "completed"
		}
	}
	w.mu.Unlock()
	if step == "start" {
		w.queue.Enqueue("workflow", map[string]interface{}{"run_id": runID, "step": "complete"})
	}
	if step == "complete" {
		w.stream.Publish("workflows", runID, `{"status":"completed"}`)
	}
}

type QueueService struct{ broker *QueueBroker }

func (q QueueService) Enqueue(ctx *Context) error {
	name := ctx.Params["name"]
	payload := getObj(ctx.Body, "payload")
	msg := q.broker.Enqueue(name, payload)
	JSON(ctx.W, http.StatusCreated, msg)
	return nil
}

func (q QueueService) Dequeue(ctx *Context) error {
	name := ctx.Params["name"]
	msgs := q.broker.Dequeue(name, 1)
	JSON(ctx.W, http.StatusOK, map[string]interface{}{"messages": msgs})
	return nil
}

func (q QueueService) Ack(ctx *Context) error {
	id := getStr(ctx.Body, "message_id")
	success := getBool(ctx.Body, "success", true)
	q.broker.Ack(id, success)
	JSON(ctx.W, http.StatusOK, map[string]interface{}{"status": "ok"})
	return nil
}

type StreamService struct{ broker *StreamBroker }

func (s StreamService) Publish(ctx *Context) error {
	topic := ctx.Params["topic"]
	key := getStr(ctx.Body, "key")
	value := fmt.Sprintf("%v", ctx.Body["value"])
	record := s.broker.Publish(topic, key, value)
	JSON(ctx.W, http.StatusOK, record)
	return nil
}

func (s StreamService) Consume(ctx *Context) error {
	topic := ctx.Params["topic"]
	group := getStr(ctx.Body, "group")
	if group == "" {
		group = "default"
	}
	records := s.broker.Consume(topic, group, 10)
	JSON(ctx.W, http.StatusOK, map[string]interface{}{"records": records})
	return nil
}

func (s StreamService) Commit(ctx *Context) error {
	topic := ctx.Params["topic"]
	group := getStr(ctx.Body, "group")
	partition := int(getFloat(ctx.Body, "partition"))
	offset := int64(getFloat(ctx.Body, "offset"))
	s.broker.Commit(topic, group, partition, offset)
	JSON(ctx.W, http.StatusOK, map[string]interface{}{"status": "ok"})
	return nil
}

type CacheService struct{ cache *CacheStore }

func (c CacheService) Get(ctx *Context) error {
	key := ctx.Params["key"]
	val, ok := c.cache.Get(key)
	if !ok {
		return ApiError{Status: http.StatusNotFound, Code: "cache_miss", Message: "Cache miss"}
	}
	JSON(ctx.W, http.StatusOK, map[string]interface{}{"key": key, "value": val})
	return nil
}

func (c CacheService) Put(ctx *Context) error {
	key := ctx.Params["key"]
	value := getStr(ctx.Body, "value")
	ttl := int64(getFloat(ctx.Body, "ttl_seconds"))
	c.cache.Put(key, value, ttl)
	JSON(ctx.W, http.StatusOK, map[string]interface{}{"status": "ok"})
	return nil
}

func (c CacheService) Delete(ctx *Context) error {
	key := ctx.Params["key"]
	c.cache.Delete(key)
	JSON(ctx.W, http.StatusOK, map[string]interface{}{"status": "ok"})
	return nil
}

type DatabaseService struct {
	users map[string]map[string]interface{}
	docs  *DocumentStore
	mu    sync.Mutex
}

func NewDatabaseService(docs *DocumentStore) *DatabaseService {
	return &DatabaseService{users: map[string]map[string]interface{}{}, docs: docs}
}

func (d *DatabaseService) Query(ctx *Context) error {
	sql := getStr(ctx.Body, "sql")
	if strings.Contains(strings.ToLower(sql), "from users") {
		id := ""
		if idx := strings.Index(sql, "id ="); idx != -1 {
			id = strings.Trim(strings.TrimSpace(sql[idx+4:]), " ?")
		}
		if id != "" {
			d.mu.Lock()
			user := d.users[id]
			d.mu.Unlock()
			if user == nil {
				JSON(ctx.W, http.StatusOK, map[string]interface{}{"rows": []map[string]interface{}{}})
				return nil
			}
			JSON(ctx.W, http.StatusOK, map[string]interface{}{"rows": []map[string]interface{}{user}})
			return nil
		}
	}
	return ApiError{Status: http.StatusBadRequest, Code: "unsupported_sql", Message: "Unsupported SQL in demo engine"}
}

func (d *DatabaseService) Execute(ctx *Context) error {
	sql := strings.ToLower(getStr(ctx.Body, "sql"))
	if strings.HasPrefix(sql, "insert into users") {
		id := newID("usr")
		d.mu.Lock()
		d.users[id] = map[string]interface{}{"id": id}
		d.mu.Unlock()
		JSON(ctx.W, http.StatusOK, map[string]interface{}{"status": "ok"})
		return nil
	}
	return ApiError{Status: http.StatusBadRequest, Code: "unsupported_sql", Message: "Unsupported SQL in demo engine"}
}

func (d *DatabaseService) DocumentGet(ctx *Context) error {
	collection := getStr(ctx.Body, "collection")
	key := getStr(ctx.Body, "key")
	doc, ok := d.docs.Get(collection, key)
	if !ok {
		return ApiError{Status: http.StatusNotFound, Code: "doc_not_found", Message: "Document not found"}
	}
	JSON(ctx.W, http.StatusOK, map[string]interface{}{"document": doc})
	return nil
}

func (d *DatabaseService) DocumentPut(ctx *Context) error {
	collection := getStr(ctx.Body, "collection")
	key := getStr(ctx.Body, "key")
	doc := getObj(ctx.Body, "document")
	d.docs.Put(collection, key, doc)
	JSON(ctx.W, http.StatusOK, map[string]interface{}{"status": "ok"})
	return nil
}

type SchedulerEngine struct {
	mu        sync.Mutex
	schedules map[string]map[string]interface{}
	queue     *QueueBroker
	stop      chan struct{}
}

func NewSchedulerEngine(queue *QueueBroker) *SchedulerEngine {
	return &SchedulerEngine{schedules: map[string]map[string]interface{}{}, queue: queue, stop: make(chan struct{})}
}

func (s *SchedulerEngine) Create(cron string, payload map[string]interface{}) string {
	id := newID("sched")
	s.mu.Lock()
	s.schedules[id] = map[string]interface{}{"cron": cron, "payload": payload, "enabled": true, "next_run": time.Now().Add(5 * time.Second)}
	s.mu.Unlock()
	return id
}

func (s *SchedulerEngine) SetEnabled(id string, enabled bool) {
	s.mu.Lock()
	if s.schedules[id] != nil {
		s.schedules[id]["enabled"] = enabled
	}
	s.mu.Unlock()
}

func (s *SchedulerEngine) Start() {
	go func() {
		ticker := time.NewTicker(1 * time.Second)
		defer ticker.Stop()
		for {
			select {
			case <-ticker.C:
				now := time.Now()
				s.mu.Lock()
				for id, sched := range s.schedules {
					if sched["enabled"].(bool) && sched["next_run"].(time.Time).Before(now) {
						s.queue.Enqueue("scheduler", map[string]interface{}{"schedule_id": id, "payload": sched["payload"]})
						sched["next_run"] = now.Add(60 * time.Second)
					}
				}
				s.mu.Unlock()
			case <-s.stop:
				return
			}
		}
	}()
}

type SchedulerService struct{ engine *SchedulerEngine }

func (s SchedulerService) Create(ctx *Context) error {
	cron := getStr(ctx.Body, "cron")
	payload := getObj(ctx.Body, "payload")
	id := s.engine.Create(cron, payload)
	JSON(ctx.W, http.StatusCreated, map[string]interface{}{"schedule_id": id})
	return nil
}

func (s SchedulerService) Enable(ctx *Context) error {
	id := ctx.Params["id"]
	s.engine.SetEnabled(id, true)
	JSON(ctx.W, http.StatusOK, map[string]interface{}{"status": "ok"})
	return nil
}

func (s SchedulerService) Disable(ctx *Context) error {
	id := ctx.Params["id"]
	s.engine.SetEnabled(id, false)
	JSON(ctx.W, http.StatusOK, map[string]interface{}{"status": "ok"})
	return nil
}

type WorkerFleet struct {
	queue    *QueueBroker
	payment  *PaymentService
	workflow *WorkflowEngine
	logger   Logger
	pool     chan map[string]interface{}
}

func NewWorkerFleet(queue *QueueBroker, payment *PaymentService, workflow *WorkflowEngine, logger Logger) *WorkerFleet {
	return &WorkerFleet{
		queue:    queue,
		payment:  payment,
		workflow: workflow,
		logger:   logger,
		pool:     make(chan map[string]interface{}, 64),
	}
}

func (w *WorkerFleet) Start(concurrency int) {
	for i := 0; i < concurrency; i++ {
		go func() {
			for msg := range w.pool {
				queueName, _ := msg["queue"].(string)
				defer w.queue.Ack(msg["id"].(string), true)
				if queueName == "payments" {
					w.payment.ProcessCharge(msg["payload"].(map[string]interface{}))
				}
				if queueName == "workflow" {
					w.workflow.ProcessTask(msg["payload"].(map[string]interface{}))
				}
			}
		}()
	}
	go func() {
		for {
			for _, name := range []string{"payments", "workflow", "scheduler"} {
				msgs := w.queue.Dequeue(name, 2)
				for _, msg := range msgs {
					w.pool <- msg
				}
			}
			time.Sleep(500 * time.Millisecond)
		}
	}()
}

type WorkerService struct{}

func (w WorkerService) Register(ctx *Context) error {
	JSON(ctx.W, http.StatusOK, map[string]interface{}{"status": "ok"})
	return nil
}

func (w WorkerService) Heartbeat(ctx *Context) error {
	JSON(ctx.W, http.StatusOK, map[string]interface{}{"status": "ok"})
	return nil
}

func (w WorkerService) TaskResult(ctx *Context) error {
	JSON(ctx.W, http.StatusOK, map[string]interface{}{"status": "ok"})
	return nil
}

type WebSocketService struct{ hub *WebSocketHub }

func (w WebSocketService) Publish(ctx *Context) error {
	payloadBytes, _ := json.Marshal(ctx.Body["payload"])
	w.hub.Publish(string(payloadBytes))
	JSON(ctx.W, http.StatusOK, map[string]interface{}{"status": "ok"})
	return nil
}

func (w WebSocketService) Upgrade(ctx *Context) error {
	hj, ok := ctx.W.(http.Hijacker)
	if !ok {
		return ApiError{Status: http.StatusInternalServerError, Code: "hijack_error", Message: "websocket unsupported"}
	}
	conn, _, err := hj.Hijack()
	if err != nil {
		return ApiError{Status: http.StatusInternalServerError, Code: "hijack_error", Message: "websocket failed"}
	}
	key := ctx.R.Header.Get("Sec-WebSocket-Key")
	if key == "" {
		_ = conn.Close()
		return errors.New("missing websocket key")
	}
	accept := wsAcceptKey(key)
	response := "HTTP/1.1 101 Switching Protocols\r\n" +
		"Upgrade: websocket\r\n" +
		"Connection: Upgrade\r\n" +
		"Sec-WebSocket-Accept: " + accept + "\r\n\r\n"
	_, _ = conn.Write([]byte(response))
	wsConn := &WSConnection{conn: conn}
	w.hub.Register(wsConn)
	return nil
}

func wsAcceptKey(key string) string {
	const guid = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
	sum := sha1.Sum([]byte(key + guid))
	return base64.StdEncoding.EncodeToString(sum[:])
}

// ---------------------------
// API Gateway
// ---------------------------

type HttpClient struct {
	BaseURL string
}

func (c HttpClient) Request(method, path string, body map[string]interface{}, headers map[string]string) (map[string]interface{}, error) {
	data, _ := json.Marshal(body)
	req, _ := http.NewRequest(method, c.BaseURL+path, bytes.NewReader(data))
	req.Header.Set("Content-Type", "application/json")
	for k, v := range headers {
		req.Header.Set(k, v)
	}
	client := http.Client{Timeout: 3 * time.Second}
	var respBody map[string]interface{}
	err := withRetry(func() error {
		resp, err := client.Do(req)
		if err != nil {
			return err
		}
		defer resp.Body.Close()
		b, _ := io.ReadAll(resp.Body)
		_ = json.Unmarshal(b, &respBody)
		return nil
	}, 3)
	return respBody, err
}

type AuthClient struct{ http HttpClient }

func (c AuthClient) Authorize(clientID, redirectURI, scope, userID, state string) (map[string]interface{}, error) {
	return c.http.Request("POST", "/auth/oauth/authorize", map[string]interface{}{
		"client_id": clientID, "redirect_uri": redirectURI, "scope": scope, "user_id": userID, "state": state,
	}, map[string]string{})
}

func (c AuthClient) Token(code, clientID, clientSecret string) (map[string]interface{}, error) {
	return c.http.Request("POST", "/auth/oauth/token", map[string]interface{}{
		"grant_type": "authorization_code", "code": code, "client_id": clientID, "client_secret": clientSecret,
	}, map[string]string{})
}

func (c AuthClient) Refresh(refreshToken string) (map[string]interface{}, error) {
	return c.http.Request("POST", "/auth/token/refresh", map[string]interface{}{"refresh_token": refreshToken}, map[string]string{})
}

func (c AuthClient) EnrollMfa(userID string) (map[string]interface{}, error) {
	return c.http.Request("POST", "/auth/mfa/enroll", map[string]interface{}{"user_id": userID}, map[string]string{})
}

func (c AuthClient) VerifyMfa(userID, code string) (map[string]interface{}, error) {
	return c.http.Request("POST", "/auth/mfa/verify", map[string]interface{}{"user_id": userID, "code": code}, map[string]string{})
}

type UserClient struct{ http HttpClient }

func (c UserClient) Register(email, displayName string) (map[string]interface{}, error) {
	return c.http.Request("POST", "/users/register", map[string]interface{}{"email": email, "display_name": displayName}, map[string]string{})
}

func (c UserClient) Get(userID string) (map[string]interface{}, error) {
	return c.http.Request("GET", "/users/"+userID, map[string]interface{}{}, map[string]string{})
}

func (c UserClient) Update(userID, displayName, status string) (map[string]interface{}, error) {
	return c.http.Request("PATCH", "/users/"+userID, map[string]interface{}{"display_name": displayName, "status": status}, map[string]string{})
}

type PaymentClient struct{ http HttpClient }

func (c PaymentClient) CreateIntent(userID string, amount int64, currency, idempotencyKey string) (map[string]interface{}, error) {
	return c.http.Request("POST", "/payments/intents", map[string]interface{}{
		"user_id": userID, "amount": amount, "currency": currency, "idempotency_key": idempotencyKey,
	}, map[string]string{})
}

func (c PaymentClient) GetIntent(intentID string) (map[string]interface{}, error) {
	return c.http.Request("GET", "/payments/intents/"+intentID, map[string]interface{}{}, map[string]string{})
}

func (c PaymentClient) CaptureIntent(intentID string) (map[string]interface{}, error) {
	return c.http.Request("POST", "/payments/intents/"+intentID+"/capture", map[string]interface{}{}, map[string]string{})
}

func (c PaymentClient) RefundIntent(intentID string, amount int64) (map[string]interface{}, error) {
	return c.http.Request("POST", "/payments/intents/"+intentID+"/refund", map[string]interface{}{"amount": amount}, map[string]string{})
}

type WorkflowClient struct{ http HttpClient }

func (c WorkflowClient) Register(name string, definition map[string]interface{}) (map[string]interface{}, error) {
	return c.http.Request("POST", "/workflows", map[string]interface{}{"name": name, "definition": definition}, map[string]string{})
}

func (c WorkflowClient) Start(workflowID string, payload map[string]interface{}) (map[string]interface{}, error) {
	return c.http.Request("POST", "/workflows/"+workflowID+"/start", map[string]interface{}{"input": payload}, map[string]string{})
}

func (c WorkflowClient) GetRun(runID string) (map[string]interface{}, error) {
	return c.http.Request("GET", "/workflows/runs/"+runID, map[string]interface{}{}, map[string]string{})
}

type QueueClient struct{ http HttpClient }

func (c QueueClient) Enqueue(name string, payload map[string]interface{}) (map[string]interface{}, error) {
	return c.http.Request("POST", "/queues/"+name+"/enqueue", map[string]interface{}{"payload": payload}, map[string]string{})
}

func (c QueueClient) Dequeue(name string) (map[string]interface{}, error) {
	return c.http.Request("POST", "/queues/"+name+"/dequeue", map[string]interface{}{}, map[string]string{})
}

func (c QueueClient) Ack(name, messageID string, success bool) (map[string]interface{}, error) {
	return c.http.Request("POST", "/queues/"+name+"/ack", map[string]interface{}{"message_id": messageID, "success": success}, map[string]string{})
}

type StreamClient struct{ http HttpClient }

func (c StreamClient) Publish(topic, key string, value map[string]interface{}) (map[string]interface{}, error) {
	return c.http.Request("POST", "/streams/"+topic+"/publish", map[string]interface{}{"key": key, "value": value}, map[string]string{})
}

func (c StreamClient) Consume(topic, group string) (map[string]interface{}, error) {
	return c.http.Request("GET", "/streams/"+topic+"/consume", map[string]interface{}{"group": group}, map[string]string{})
}

func (c StreamClient) Commit(topic, group string, partition int, offset int64) (map[string]interface{}, error) {
	return c.http.Request("POST", "/streams/"+topic+"/commit", map[string]interface{}{"group": group, "partition": partition, "offset": offset}, map[string]string{})
}

type CacheClient struct{ http HttpClient }

func (c CacheClient) Get(key string) (map[string]interface{}, error) {
	return c.http.Request("GET", "/cache/"+key, map[string]interface{}{}, map[string]string{})
}

func (c CacheClient) Put(key, value string, ttl int64) (map[string]interface{}, error) {
	return c.http.Request("PUT", "/cache/"+key, map[string]interface{}{"value": value, "ttl_seconds": ttl}, map[string]string{})
}

func (c CacheClient) Delete(key string) (map[string]interface{}, error) {
	return c.http.Request("DELETE", "/cache/"+key, map[string]interface{}{}, map[string]string{})
}

type DatabaseClient struct{ http HttpClient }

func (c DatabaseClient) Query(sql string, params []interface{}) (map[string]interface{}, error) {
	return c.http.Request("POST", "/db/query", map[string]interface{}{"sql": sql, "params": params}, map[string]string{})
}

func (c DatabaseClient) Execute(sql string, params []interface{}) (map[string]interface{}, error) {
	return c.http.Request("POST", "/db/execute", map[string]interface{}{"sql": sql, "params": params}, map[string]string{})
}

func (c DatabaseClient) DocumentGet(collection, key string) (map[string]interface{}, error) {
	return c.http.Request("POST", "/db/document/get", map[string]interface{}{"collection": collection, "key": key}, map[string]string{})
}

func (c DatabaseClient) DocumentPut(collection, key string, doc map[string]interface{}) (map[string]interface{}, error) {
	return c.http.Request("POST", "/db/document/put", map[string]interface{}{"collection": collection, "key": key, "document": doc}, map[string]string{})
}

type WebSocketClient struct{ http HttpClient }

func (c WebSocketClient) Publish(payload map[string]interface{}) (map[string]interface{}, error) {
	return c.http.Request("POST", "/ws/publish", map[string]interface{}{"payload": payload}, map[string]string{})
}

type SchedulerClient struct{ http HttpClient }

func (c SchedulerClient) Create(cron string, payload map[string]interface{}) (map[string]interface{}, error) {
	return c.http.Request("POST", "/schedules", map[string]interface{}{"cron": cron, "payload": payload}, map[string]string{})
}

func (c SchedulerClient) Enable(id string) (map[string]interface{}, error) {
	return c.http.Request("POST", "/schedules/"+id+"/enable", map[string]interface{}{}, map[string]string{})
}

func (c SchedulerClient) Disable(id string) (map[string]interface{}, error) {
	return c.http.Request("POST", "/schedules/"+id+"/disable", map[string]interface{}{}, map[string]string{})
}

type WorkerClient struct{ http HttpClient }

func (c WorkerClient) Register(workerID string, capabilities map[string]interface{}) (map[string]interface{}, error) {
	return c.http.Request("POST", "/workers/register", map[string]interface{}{"worker_id": workerID, "capabilities": capabilities}, map[string]string{})
}

func (c WorkerClient) Heartbeat(workerID string) (map[string]interface{}, error) {
	return c.http.Request("POST", "/workers/heartbeat", map[string]interface{}{"worker_id": workerID}, map[string]string{})
}

func (c WorkerClient) TaskResult(taskID, status string, output map[string]interface{}) (map[string]interface{}, error) {
	return c.http.Request("POST", "/workers/task/result", map[string]interface{}{"task_id": taskID, "status": status, "output": output}, map[string]string{})
}

type ApiGateway struct {
	clients map[string]HttpClient
}

func NewApiGateway(cfg Config) *ApiGateway {
	return &ApiGateway{clients: map[string]HttpClient{
		"auth":      {BaseURL: fmt.Sprintf("http://127.0.0.1:%d", cfg.AuthPort)},
		"user":      {BaseURL: fmt.Sprintf("http://127.0.0.1:%d", cfg.UserPort)},
		"payment":   {BaseURL: fmt.Sprintf("http://127.0.0.1:%d", cfg.PaymentPort)},
		"workflow":  {BaseURL: fmt.Sprintf("http://127.0.0.1:%d", cfg.WorkflowPort)},
		"queue":     {BaseURL: fmt.Sprintf("http://127.0.0.1:%d", cfg.QueuePort)},
		"stream":    {BaseURL: fmt.Sprintf("http://127.0.0.1:%d", cfg.StreamPort)},
		"cache":     {BaseURL: fmt.Sprintf("http://127.0.0.1:%d", cfg.CachePort)},
		"db":        {BaseURL: fmt.Sprintf("http://127.0.0.1:%d", cfg.DBPort)},
		"ws":        {BaseURL: fmt.Sprintf("http://127.0.0.1:%d", cfg.WSPort)},
		"scheduler": {BaseURL: fmt.Sprintf("http://127.0.0.1:%d", cfg.SchedulerPort)},
		"worker":    {BaseURL: fmt.Sprintf("http://127.0.0.1:%d", cfg.WorkerPort)},
	}}
}

func (g *ApiGateway) Forward(service string, ctx *Context) error {
	headers := map[string]string{}
	if ctx.CorrelationID != "" {
		headers["Correlation-Id"] = ctx.CorrelationID
	}
	if ctx.IdempotencyKey != "" {
		headers["Idempotency-Key"] = ctx.IdempotencyKey
	}
	resp, err := g.clients[service].Request(ctx.R.Method, ctx.R.URL.Path, ctx.Body, headers)
	if err != nil {
		return ApiError{Status: http.StatusBadGateway, Code: "upstream_error", Message: "Upstream error", Retryable: true}
	}
	JSON(ctx.W, http.StatusOK, resp)
	return nil
}

// ---------------------------
// Helpers
// ---------------------------

func getStr(m map[string]interface{}, key string) string {
	if v, ok := m[key]; ok {
		return fmt.Sprintf("%v", v)
	}
	return ""
}

func getObj(m map[string]interface{}, key string) map[string]interface{} {
	if v, ok := m[key].(map[string]interface{}); ok {
		return v
	}
	return map[string]interface{}{}
}

func getFloat(m map[string]interface{}, key string) float64 {
	if v, ok := m[key].(float64); ok {
		return v
	}
	return 0
}

func getBool(m map[string]interface{}, key string, def bool) bool {
	if v, ok := m[key].(bool); ok {
		return v
	}
	return def
}

func buildRouter(logger Logger, metrics *Metrics, limiter *RateLimiter, authSecret string) *Router {
	router := &Router{}
	base := []Middleware{middlewareLogging(logger, metrics), middlewareRateLimit(limiter)}
	router.Add("GET", "/healthz", func(ctx *Context) error {
		JSON(ctx.W, http.StatusOK, map[string]interface{}{"status": "ok"})
		return nil
	}, base...)
	router.Add("GET", "/readyz", func(ctx *Context) error {
		JSON(ctx.W, http.StatusOK, map[string]interface{}{"status": "ready"})
		return nil
	}, base...)
	router.Add("GET", "/metrics", func(ctx *Context) error {
		_, _ = ctx.W.Write([]byte(metrics.Render()))
		return nil
	}, base...)
	if authSecret != "" {
		base = append(base, middlewareAuth(authSecret))
	}
	return router
}

func startServer(port int, router *Router) {
	go func() {
		_ = http.ListenAndServe(fmt.Sprintf(":%d", port), router)
	}()
}

func main() {
	cfg := LoadConfig()
	metrics := NewMetrics()
	limiter := NewRateLimiter(cfg.RateLimitPerMin)

	isEnabled := func(name string) bool {
		if len(cfg.ServiceOnly) == 0 {
			return true
		}
		for _, svc := range cfg.ServiceOnly {
			if svc == name {
				return true
			}
		}
		return false
	}

	authService := NewAuthService(cfg)
	authService.RegisterClient("platform_cli", "platform_secret")
	userService := NewUserService()
	queueBroker := NewQueueBroker()
	streamBroker := NewStreamBroker()
	idem := NewIdempotencyStore()
	paymentService := NewPaymentService(queueBroker, streamBroker, idem)
	workflowEngine := NewWorkflowEngine(queueBroker, streamBroker)
	cacheStore := NewCacheStore()
	docStore := NewDocumentStore()
	dbService := NewDatabaseService(docStore)
	scheduler := NewSchedulerEngine(queueBroker)
	if isEnabled("scheduler") {
		scheduler.Start()
	}
	workerFleet := NewWorkerFleet(queueBroker, paymentService, workflowEngine, Logger{Service: "workers"})
	if isEnabled("worker") {
		workerFleet.Start(cfg.WorkerConcurrency)
	}
	wsHub := NewWebSocketHub()

	// Auth router
	authRouter := buildRouter(Logger{Service: "auth"}, metrics, limiter, "")
	authRouter.Add("POST", "/auth/oauth/authorize", authService.Authorize)
	authRouter.Add("POST", "/auth/oauth/token", authService.Token)
	authRouter.Add("POST", "/auth/token/refresh", authService.Refresh)
	authRouter.Add("POST", "/auth/mfa/enroll", authService.EnrollMfa)
	authRouter.Add("POST", "/auth/mfa/verify", authService.VerifyMfa)

	// User router
	userRouter := buildRouter(Logger{Service: "user"}, metrics, limiter, cfg.JWTSecret)
	userRouter.Add("POST", "/users/register", userService.Register)
	userRouter.Add("GET", "/users/{id}", userService.Get)
	userRouter.Add("PATCH", "/users/{id}", userService.Update)

	// Payment router
	paymentRouter := buildRouter(Logger{Service: "payment"}, metrics, limiter, cfg.JWTSecret)
	paymentRouter.Add("POST", "/payments/intents", paymentService.CreateIntent)
	paymentRouter.Add("GET", "/payments/intents/{id}", paymentService.GetIntent)
	paymentRouter.Add("POST", "/payments/intents/{id}/capture", paymentService.CaptureIntent)
	paymentRouter.Add("POST", "/payments/intents/{id}/refund", paymentService.RefundIntent)

	// Workflow router
	workflowRouter := buildRouter(Logger{Service: "workflow"}, metrics, limiter, cfg.JWTSecret)
	workflowRouter.Add("POST", "/workflows", workflowEngine.Register)
	workflowRouter.Add("POST", "/workflows/{id}/start", workflowEngine.Start)
	workflowRouter.Add("GET", "/workflows/runs/{run_id}", workflowEngine.GetRun)

	// Queue router
	queueRouter := buildRouter(Logger{Service: "queue"}, metrics, limiter, cfg.JWTSecret)
	queueRouter.Add("POST", "/queues/{name}/enqueue", QueueService{broker: queueBroker}.Enqueue)
	queueRouter.Add("POST", "/queues/{name}/dequeue", QueueService{broker: queueBroker}.Dequeue)
	queueRouter.Add("POST", "/queues/{name}/ack", QueueService{broker: queueBroker}.Ack)

	// Stream router
	streamRouter := buildRouter(Logger{Service: "stream"}, metrics, limiter, cfg.JWTSecret)
	streamRouter.Add("POST", "/streams/{topic}/publish", StreamService{broker: streamBroker}.Publish)
	streamRouter.Add("GET", "/streams/{topic}/consume", StreamService{broker: streamBroker}.Consume)
	streamRouter.Add("POST", "/streams/{topic}/commit", StreamService{broker: streamBroker}.Commit)

	// Cache router
	cacheRouter := buildRouter(Logger{Service: "cache"}, metrics, limiter, cfg.JWTSecret)
	cacheRouter.Add("GET", "/cache/{key}", CacheService{cache: cacheStore}.Get)
	cacheRouter.Add("PUT", "/cache/{key}", CacheService{cache: cacheStore}.Put)
	cacheRouter.Add("DELETE", "/cache/{key}", CacheService{cache: cacheStore}.Delete)

	// Database router
	dbRouter := buildRouter(Logger{Service: "db"}, metrics, limiter, cfg.JWTSecret)
	dbRouter.Add("POST", "/db/query", dbService.Query)
	dbRouter.Add("POST", "/db/execute", dbService.Execute)
	dbRouter.Add("POST", "/db/document/get", dbService.DocumentGet)
	dbRouter.Add("POST", "/db/document/put", dbService.DocumentPut)

	// WebSocket router
	wsRouter := buildRouter(Logger{Service: "ws"}, metrics, limiter, cfg.JWTSecret)
	wsRouter.Add("POST", "/ws/publish", WebSocketService{hub: wsHub}.Publish)
	wsRouter.Add("GET", "/ws", WebSocketService{hub: wsHub}.Upgrade)

	// Scheduler router
	schedulerRouter := buildRouter(Logger{Service: "scheduler"}, metrics, limiter, cfg.JWTSecret)
	schedulerRouter.Add("POST", "/schedules", SchedulerService{engine: scheduler}.Create)
	schedulerRouter.Add("POST", "/schedules/{id}/enable", SchedulerService{engine: scheduler}.Enable)
	schedulerRouter.Add("POST", "/schedules/{id}/disable", SchedulerService{engine: scheduler}.Disable)

	// Worker router
	workerRouter := buildRouter(Logger{Service: "worker"}, metrics, limiter, cfg.JWTSecret)
	workerRouter.Add("POST", "/workers/register", WorkerService{}.Register)
	workerRouter.Add("POST", "/workers/heartbeat", WorkerService{}.Heartbeat)
	workerRouter.Add("POST", "/workers/task/result", WorkerService{}.TaskResult)

	// Gateway router
	gateway := NewApiGateway(cfg)
	gatewayRouter := buildRouter(Logger{Service: "gateway"}, metrics, limiter, "")
	gatewayRouter.Add("POST", "/auth/oauth/authorize", func(ctx *Context) error { return gateway.Forward("auth", ctx) })
	gatewayRouter.Add("POST", "/auth/oauth/token", func(ctx *Context) error { return gateway.Forward("auth", ctx) })
	gatewayRouter.Add("POST", "/auth/token/refresh", func(ctx *Context) error { return gateway.Forward("auth", ctx) })
	gatewayRouter.Add("POST", "/auth/mfa/enroll", func(ctx *Context) error { return gateway.Forward("auth", ctx) })
	gatewayRouter.Add("POST", "/auth/mfa/verify", func(ctx *Context) error { return gateway.Forward("auth", ctx) })
	gatewayRouter.Add("POST", "/users/register", func(ctx *Context) error { return gateway.Forward("user", ctx) })
	gatewayRouter.Add("GET", "/users/{id}", func(ctx *Context) error { return gateway.Forward("user", ctx) })
	gatewayRouter.Add("PATCH", "/users/{id}", func(ctx *Context) error { return gateway.Forward("user", ctx) })
	gatewayRouter.Add("POST", "/payments/intents", func(ctx *Context) error { return gateway.Forward("payment", ctx) })
	gatewayRouter.Add("GET", "/payments/intents/{id}", func(ctx *Context) error { return gateway.Forward("payment", ctx) })
	gatewayRouter.Add("POST", "/payments/intents/{id}/capture", func(ctx *Context) error { return gateway.Forward("payment", ctx) })
	gatewayRouter.Add("POST", "/payments/intents/{id}/refund", func(ctx *Context) error { return gateway.Forward("payment", ctx) })
	gatewayRouter.Add("POST", "/workflows", func(ctx *Context) error { return gateway.Forward("workflow", ctx) })
	gatewayRouter.Add("POST", "/workflows/{id}/start", func(ctx *Context) error { return gateway.Forward("workflow", ctx) })
	gatewayRouter.Add("GET", "/workflows/runs/{run_id}", func(ctx *Context) error { return gateway.Forward("workflow", ctx) })
	gatewayRouter.Add("POST", "/queues/{name}/enqueue", func(ctx *Context) error { return gateway.Forward("queue", ctx) })
	gatewayRouter.Add("POST", "/queues/{name}/dequeue", func(ctx *Context) error { return gateway.Forward("queue", ctx) })
	gatewayRouter.Add("POST", "/queues/{name}/ack", func(ctx *Context) error { return gateway.Forward("queue", ctx) })
	gatewayRouter.Add("POST", "/streams/{topic}/publish", func(ctx *Context) error { return gateway.Forward("stream", ctx) })
	gatewayRouter.Add("GET", "/streams/{topic}/consume", func(ctx *Context) error { return gateway.Forward("stream", ctx) })
	gatewayRouter.Add("POST", "/streams/{topic}/commit", func(ctx *Context) error { return gateway.Forward("stream", ctx) })
	gatewayRouter.Add("GET", "/cache/{key}", func(ctx *Context) error { return gateway.Forward("cache", ctx) })
	gatewayRouter.Add("PUT", "/cache/{key}", func(ctx *Context) error { return gateway.Forward("cache", ctx) })
	gatewayRouter.Add("DELETE", "/cache/{key}", func(ctx *Context) error { return gateway.Forward("cache", ctx) })
	gatewayRouter.Add("POST", "/db/query", func(ctx *Context) error { return gateway.Forward("db", ctx) })
	gatewayRouter.Add("POST", "/db/execute", func(ctx *Context) error { return gateway.Forward("db", ctx) })
	gatewayRouter.Add("POST", "/db/document/get", func(ctx *Context) error { return gateway.Forward("db", ctx) })
	gatewayRouter.Add("POST", "/db/document/put", func(ctx *Context) error { return gateway.Forward("db", ctx) })
	gatewayRouter.Add("POST", "/ws/publish", func(ctx *Context) error { return gateway.Forward("ws", ctx) })
	gatewayRouter.Add("POST", "/schedules", func(ctx *Context) error { return gateway.Forward("scheduler", ctx) })
	gatewayRouter.Add("POST", "/schedules/{id}/enable", func(ctx *Context) error { return gateway.Forward("scheduler", ctx) })
	gatewayRouter.Add("POST", "/schedules/{id}/disable", func(ctx *Context) error { return gateway.Forward("scheduler", ctx) })
	gatewayRouter.Add("POST", "/workers/register", func(ctx *Context) error { return gateway.Forward("worker", ctx) })
	gatewayRouter.Add("POST", "/workers/heartbeat", func(ctx *Context) error { return gateway.Forward("worker", ctx) })
	gatewayRouter.Add("POST", "/workers/task/result", func(ctx *Context) error { return gateway.Forward("worker", ctx) })

	if isEnabled("auth") {
		startServer(cfg.AuthPort, authRouter)
	}
	if isEnabled("user") {
		startServer(cfg.UserPort, userRouter)
	}
	if isEnabled("payment") {
		startServer(cfg.PaymentPort, paymentRouter)
	}
	if isEnabled("workflow") {
		startServer(cfg.WorkflowPort, workflowRouter)
	}
	if isEnabled("queue") {
		startServer(cfg.QueuePort, queueRouter)
	}
	if isEnabled("stream") {
		startServer(cfg.StreamPort, streamRouter)
	}
	if isEnabled("cache") {
		startServer(cfg.CachePort, cacheRouter)
	}
	if isEnabled("db") {
		startServer(cfg.DBPort, dbRouter)
	}
	if isEnabled("ws") {
		startServer(cfg.WSPort, wsRouter)
	}
	if isEnabled("scheduler") {
		startServer(cfg.SchedulerPort, schedulerRouter)
	}
	if isEnabled("worker") {
		startServer(cfg.WorkerPort, workerRouter)
	}
	if isEnabled("gateway") {
		startServer(cfg.GatewayPort, gatewayRouter)
	}

	select {}
}
