FROM python:3.11-slim
WORKDIR /app
COPY src/python/platform.py /app/platform.py
ENV SERVICE_ONLY=auth
ENV AUTH_PORT=8081
EXPOSE 8081
CMD ["python", "/app/platform.py"]
