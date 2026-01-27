FROM python:3.11-slim
WORKDIR /app
COPY src/python/platform.py /app/platform.py
ENV SERVICE_ONLY=worker
ENV WORKER_PORT=8091
EXPOSE 8091
CMD ["python", "/app/platform.py"]
