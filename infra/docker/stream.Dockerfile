FROM python:3.11-slim
WORKDIR /app
COPY src/python/platform.py /app/platform.py
ENV SERVICE_ONLY=stream
ENV STREAM_PORT=8086
EXPOSE 8086
CMD ["python", "/app/platform.py"]
