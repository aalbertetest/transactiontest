FROM python:3.11-slim
WORKDIR /app
COPY src/python/platform.py /app/platform.py
ENV SERVICE_ONLY=cache
ENV CACHE_PORT=8087
EXPOSE 8087
CMD ["python", "/app/platform.py"]
