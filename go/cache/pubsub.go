package cache

import "sync"

type Subscriber func(payload any)

type PubSub struct {
	mu   sync.RWMutex
	subs map[string][]Subscriber
}

func NewPubSub() *PubSub {
	return &PubSub{subs: map[string][]Subscriber{}}
}

func (p *PubSub) Subscribe(channel string, handler Subscriber) func() {
	p.mu.Lock()
	p.subs[channel] = append(p.subs[channel], handler)
	p.mu.Unlock()
	return func() {
		p.mu.Lock()
		defer p.mu.Unlock()
		handlers := p.subs[channel]
		for i, h := range handlers {
			if h == handler {
				p.subs[channel] = append(handlers[:i], handlers[i+1:]...)
				break
			}
		}
	}
}

func (p *PubSub) Publish(channel string, payload any) int {
	p.mu.RLock()
	handlers := append([]Subscriber{}, p.subs[channel]...)
	p.mu.RUnlock()
	for _, handler := range handlers {
		handler(payload)
	}
	return len(handlers)
}
