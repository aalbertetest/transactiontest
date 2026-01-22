import { createHash } from "crypto";

export const hashRequest = (path: string, body: Buffer) =>
  createHash("sha256").update(`${path}:`).update(body).digest("hex");
