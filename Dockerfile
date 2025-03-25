FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000 \
    HEALTH_CHECK=true

# Create and set working directory
WORKDIR /app

# Install system dependencies (combined RUN commands)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    wait-for-it \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Health check endpoint verification (pre-startup check)
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:$PORT/health/ || exit 1

# Run the application with proper startup sequence
CMD ["sh", "-c", "\
    wait-for-it --timeout=30 localhost:$PORT -- \
    gunicorn financial_audit_system.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --env HEALTH_CHECK=$HEALTH_CHECK"]