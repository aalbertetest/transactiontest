package cache

type Replicator struct {
	transport Transport
}

func NewReplicator(transport Transport) *Replicator {
	return &Replicator{transport: transport}
}

func (r *Replicator) Replicate(peers []string, message ReplicationMessage) {
	if r == nil || r.transport == nil {
		return
	}
	for _, peer := range peers {
		_ = r.transport.Send(peer, message)
	}
}
