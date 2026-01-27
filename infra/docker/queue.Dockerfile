FROM python:3.11-slim
WORKDIR /app
COPY src/python/platform.py /app/platform.py
ENV SERVICE_ONLY=queue
ENV QUEUE_PORT=8085
EXPOSE 8085
CMD ["python", "/app/platform.py"]
