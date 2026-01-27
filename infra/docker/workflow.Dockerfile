FROM python:3.11-slim
WORKDIR /app
COPY src/python/platform.py /app/platform.py
ENV SERVICE_ONLY=workflow
ENV WORKFLOW_PORT=8084
EXPOSE 8084
CMD ["python", "/app/platform.py"]
