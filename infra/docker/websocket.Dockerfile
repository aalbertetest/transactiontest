FROM python:3.11-slim
WORKDIR /app
COPY src/python/platform.py /app/platform.py
ENV SERVICE_ONLY=ws
ENV WS_PORT=8089
EXPOSE 8089
CMD ["python", "/app/platform.py"]
