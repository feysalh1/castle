#!/bin/bash
# Script to prepare the Children's Castle application for deployment

echo "===== Preparing Children's Castle for deployment ====="

# Step 1: Create Dockerfile for Cloud Run deployment
echo "Creating Dockerfile..."
cat > Dockerfile << 'EOF'
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
EOF

# Step 2: Create requirements.txt if it doesn't exist
echo "Creating requirements.txt from packages..."
pip freeze > requirements.txt

# Step 3: Copy all static files to the public directory for Firebase hosting
echo "Copying static files to public directory..."
mkdir -p public
cp -r static public/
cp -r templates public/

# Step 4: Copy application files needed for the backend
echo "Copying application files..."
mkdir -p public/app
cp *.py public/app/
cp -r .env public/app/

# Step 5: Create a cloud build configuration file
echo "Creating cloud build configuration..."
cat > cloudbuild.yaml << 'EOF'
steps:
  # Build the container image
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/childrens-castle', '.']
  # Push the container image to Container Registry
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/childrens-castle']
  # Deploy container image to Cloud Run
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: gcloud
    args:
      - 'run'
      - 'deploy'
      - 'childrens-castle'
      - '--image'
      - 'gcr.io/$PROJECT_ID/childrens-castle'
      - '--region'
      - 'us-central1'
      - '--platform'
      - 'managed'
      - '--allow-unauthenticated'
images:
  - 'gcr.io/$PROJECT_ID/childrens-castle'
EOF

echo "===== Preparation complete! ====="
echo "To deploy to Firebase Hosting with Cloud Run backend:"
echo "1. Run 'gcloud builds submit' to build and deploy the Cloud Run service"
echo "2. Run 'firebase deploy --only hosting' to deploy Firebase hosting"
echo "3. Your full application will be available at https://story-time-fun.web.app"
echo ""
echo "For more details, see the FIREBASE_DEPLOYMENT.md file."