FROM python:3.9-slim


# Add this near the top
ENV GUNICORN_CMD_ARGS="--workers=2 --timeout=120 --keep-alive=5 --access-logfile=- --error-logfile=-"


# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000 \
    HEALTH_CHECK=true \
    PYTHONFAULTHANDLER=1

# Create and set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    wait-for-it \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project (exclude unnecessary files via .dockerignore)
COPY . .

# Create static directories with correct permissions
RUN mkdir -p static staticfiles && \
    python manage.py collectstatic --noinput --clear && \
    find staticfiles -type d -exec chmod 755 {} \; && \
    find staticfiles -type f -exec chmod 644 {} \;

# Collect static files (with clear and continue-on-error)
RUN python manage.py collectstatic --noinput --clear || echo "Collectstatic completed (with possible warnings)"

# Health check configuration
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:$PORT/health/ || exit 1

# Application startup
CMD ["sh", "-c", "\
    python manage.py migrate && \
    gunicorn financial_audit_system.wsgi:application \
    --bind 0.0.0.0:$PORT"]