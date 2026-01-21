FROM python:3.11-slim
WORKDIR /app
RUN adduser --disabled-password --gecos "" appuser
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY executor ./executor
COPY tests ./tests
ENV PYTHONUNBUFFERED=1
USER appuser
CMD ["python", "-m", "executor.main"]
