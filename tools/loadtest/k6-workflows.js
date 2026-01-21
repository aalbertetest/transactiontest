import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  vus: 5,
  duration: "1m",
};

const BASE_URL = __ENV.BASE_URL || "http://localhost:8080/v1";

export default function () {
  const create = http.post(
    `${BASE_URL}/workflows`,
    JSON.stringify({
      name: `wf-${__VU}-${__ITER}`,
      description: "Load test workflow",
      spec: {
        steps: [
          { id: "echo", type: "echo", params: { message: "hi" } },
          { id: "sleep", type: "sleep", params: { seconds: 1 }, depends_on: ["echo"] },
        ],
      },
    }),
    { headers: { "Content-Type": "application/json" } }
  );

  check(create, { "workflow created": (r) => r.status === 201 });
  const workflow = JSON.parse(create.body);

  const run = http.post(
    `${BASE_URL}/workflow-runs`,
    JSON.stringify({ workflow_id: workflow.id, input: { name: "k6" } }),
    { headers: { "Content-Type": "application/json" } }
  );

  check(run, { "run created": (r) => r.status === 201 });
  sleep(1);
}
