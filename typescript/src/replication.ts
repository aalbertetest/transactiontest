import { ReplicationMessage, Transport } from "./transport";

export class Replicator {
  constructor(private transport?: Transport) {}

  replicate(peerIds: string[], message: ReplicationMessage): void {
    if (!this.transport) {
      return;
    }
    for (const peerId of peerIds) {
      this.transport.send(peerId, message);
    }
  }
}
