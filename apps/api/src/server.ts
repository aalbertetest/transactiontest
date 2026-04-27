import { createServer } from "node:http";
import { createApp } from "./app.js";
import { env } from "./config/env.js";
import { prisma } from "./db/prisma.js";
import { CollaborationServer } from "./realtime/collaboration.js";

const app = createApp();
const server = createServer(app);
const collaboration = new CollaborationServer(prisma);
collaboration.attach(server);

const shutdown = async (signal: string) => {
  console.info({ signal }, "shutting down");
  server.close(async () => {
    await prisma.$disconnect();
    process.exit(0);
  });
};

process.on("SIGTERM", () => void shutdown("SIGTERM"));
process.on("SIGINT", () => void shutdown("SIGINT"));

server.listen(env.port, () => {
  console.info(`API listening on http://localhost:${env.port}`);
});
