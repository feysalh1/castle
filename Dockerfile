FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt gunicorn psycopg2-binary python-dotenv

# Copy application code
COPY . .

# Expose port (Cloud Run will use PORT environment variable)
EXPOSE 8080
EXPOSE 5000

# Set environment variables for production
ENV PORT=8080
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production
ENV FIREBASE_STORAGE_ENABLED=true

# Start the application with proper settings for Cloud Run
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 300 main:app
