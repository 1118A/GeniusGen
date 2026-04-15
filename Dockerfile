# ── Stage 1: Build ─────────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /app

# Install system dependencies needed by psycopg2 and Pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# ── Stage 2: Production ─────────────────────────────────────────────
FROM python:3.11-slim

WORKDIR /app

# Runtime system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy project source
COPY . .

# Collect static files at build time
RUN python manage.py collectstatic --no-input

# Expose port (Koyeb uses PORT env var dynamically)
EXPOSE 8000

# Entrypoint: migrate then serve
CMD sh -c "python manage.py migrate --no-input && gunicorn geniusgen.wsgi --bind 0.0.0.0:${PORT:-8000} --workers 2 --threads 2 --timeout 120"
