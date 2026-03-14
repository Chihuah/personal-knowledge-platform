FROM python:3.11-slim

WORKDIR /app/backend

# Install system dependencies required for psycopg and database connectivity
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend ./

# Copy wait-for-db script
COPY backend/wait-for-db.py ./

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health', timeout=5)"

EXPOSE 8000

CMD ["python", "wait-for-db.py"]
