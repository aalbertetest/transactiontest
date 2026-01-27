FROM python:3.11-slim
WORKDIR /app
COPY src/python/platform.py /app/platform.py
ENV SERVICE_ONLY=user
ENV USER_PORT=8082
EXPOSE 8082
CMD ["python", "/app/platform.py"]
