FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY pyproject.toml .
COPY requirements.txt* .
COPY .env* .

# Install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt || pip3 install gunicorn flask flask-login flask-sqlalchemy flask-wtf python-dotenv openai firebase-admin elevenlabs psycopg2-binary

# Copy application code
COPY . .

# Expose port
EXPOSE 8080

# Set environment variable for production
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Start the application
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
