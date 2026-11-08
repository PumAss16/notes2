FROM python:3.11-slim AS builder
WORKDIR /app
COPY q.txt .
RUN pip install --target=/install -r q.txt
FROM python:3.11-alpine
WORKDIR /app
COPY --from=builder /install /install
COPY app.py .
ENV PYTHONPATH=/install
ENV APP_ENV=production
ENV APP_VERSION=2.0.0
CMD ["python", "app.py"]
