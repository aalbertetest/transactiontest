FROM python:3.11-slim
WORKDIR /app
COPY src/python/platform.py /app/platform.py
ENV SERVICE_ONLY=scheduler
ENV SCHEDULER_PORT=8090
EXPOSE 8090
CMD ["python", "/app/platform.py"]
