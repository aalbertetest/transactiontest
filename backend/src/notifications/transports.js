/**
 * A Transport sends a rendered message to a recipient. Adding a new transport
 * is one file: implement `send(args)` and register it in `index.js`.
 */

export class ConsoleTransport {
  async send({ to, message }) {
    // In a real deployment this would be a structured log.
    // eslint-disable-next-line no-console
    console.log(`[notify] -> ${to}\n  subject: ${message.subject}\n  body: ${message.body}`);
  }
}

export class EmailTransport {
  constructor({ send } = {}) {
    // `send` is injected so we don't take a hard dep on nodemailer here.
    this._send = send;
  }
  async send({ to, message }) {
    if (!this._send) throw new Error('email_transport_not_configured');
    await this._send({ to, subject: message.subject, body: message.body });
  }
}

export class WebhookTransport {
  constructor({ fetch: f = globalThis.fetch } = {}) {
    this._fetch = f;
  }
  async send({ to, message }) {
    const res = await this._fetch(to, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(message),
    });
    if (!res.ok) {
      throw new Error(`webhook_${res.status}`);
    }
  }
}
