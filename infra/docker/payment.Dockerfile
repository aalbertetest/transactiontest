FROM python:3.11-slim
WORKDIR /app
COPY src/python/platform.py /app/platform.py
ENV SERVICE_ONLY=payment
ENV PAYMENT_PORT=8083
EXPOSE 8083
CMD ["python", "/app/platform.py"]
