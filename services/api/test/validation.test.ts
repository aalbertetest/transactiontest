import test from "node:test";
import assert from "node:assert/strict";
import { validateWorkflowSpec } from "../src/validation.js";

test("validateWorkflowSpec rejects duplicate step ids", () => {
  const result = validateWorkflowSpec({
    steps: [
      { id: "a", type: "echo" },
      { id: "a", type: "sleep", params: { seconds: 1 } }
    ]
  });
  assert.equal(result.ok, false);
});

test("validateWorkflowSpec accepts simple workflow", () => {
  const result = validateWorkflowSpec({
    steps: [
      { id: "fetch", type: "http_request", params: { url: "https://example.com" } },
      { id: "sleep", type: "sleep", params: { seconds: 1 }, depends_on: ["fetch"] }
    ]
  });
  assert.equal(result.ok, true);
});
