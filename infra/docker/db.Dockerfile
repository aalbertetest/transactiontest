FROM python:3.11-slim
WORKDIR /app
COPY src/python/platform.py /app/platform.py
ENV SERVICE_ONLY=db
ENV DB_PORT=8088
EXPOSE 8088
CMD ["python", "/app/platform.py"]
