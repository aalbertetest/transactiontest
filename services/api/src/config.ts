export const config = {
  port: parseInt(process.env.PORT || "8080", 10),
  dbUrl: process.env.DATABASE_URL || "postgres://postgres:postgres@localhost:5432/workflow",
  serviceName: process.env.SERVICE_NAME || "workflow-api",
  maxWorkflowSteps: parseInt(process.env.MAX_WORKFLOW_STEPS || "200", 10),
  maxPayloadBytes: parseInt(process.env.MAX_PAYLOAD_BYTES || "1048576", 10)
};
