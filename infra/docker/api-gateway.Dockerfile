FROM python:3.11-slim
WORKDIR /app
COPY src/python/platform.py /app/platform.py
ENV SERVICE_ONLY=gateway
ENV GATEWAY_PORT=8080
EXPOSE 8080
CMD ["python", "/app/platform.py"]
