import { createHmac } from "crypto";

export const signPayload = (secret: string, payload: string, timestamp: number) => {
  const message = `${timestamp}.${payload}`;
  const digest = createHmac("sha256", secret).update(message).digest("hex");
  return `t=${timestamp},v1=${digest}`;
};

export const deliverWebhook = async (url: string, secret: string, event: unknown) => {
  const payload = JSON.stringify(event);
  const timestamp = Math.floor(Date.now() / 1000);
  const signature = signPayload(secret, payload, timestamp);
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Payment-Signature": signature
    },
    body: payload
  });
  if (!response.ok) {
    throw new Error(`webhook status ${response.status}`);
  }
};
