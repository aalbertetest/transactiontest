import { createApp } from "./app";
import { logger } from "./logging/logger";

const port = Number(process.env.PORT ?? 3000);
const app = createApp();

app.listen(port, () => {
  logger.info({ port }, "order api listening");
});
