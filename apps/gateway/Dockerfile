FROM python:3.11-slim as builder

WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY packages /app/packages
COPY apps/gateway /app/apps/gateway

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir /app/packages/shared && \
    pip install --no-cache-dir /app/packages/tools && \
    pip install --no-cache-dir -r /app/apps/gateway/requirements.txt


FROM python:3.11-slim as runner
WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app /app

EXPOSE 8000
CMD ["uvicorn", "apps.gateway.src.main:app", "--host", "0.0.0.0", "--port", "8000"]
