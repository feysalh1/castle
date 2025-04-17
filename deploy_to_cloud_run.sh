#!/bin/bash

# Deploy the application to Google Cloud Run
# This script should be run after the application is ready for deployment

# Configuration
PROJECT_ID="story-time-fun"
SERVICE_NAME="childrens-castle"
REGION="us-central1"
MIN_INSTANCES=0
MAX_INSTANCES=10
MEMORY="1Gi"
CPU=1
CONCURRENCY=80
TIMEOUT=300

echo "===== Starting Cloud Run Deployment ====="
echo "Deploying to project: $PROJECT_ID"
echo "Service name: $SERVICE_NAME"
echo "Region: $REGION"

# Check if gcloud CLI is available
if ! command -v gcloud &> /dev/null
then
    echo "Google Cloud SDK is not installed. Please install it first."
    exit 1
fi

# Check if user is logged in to Google Cloud
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" &> /dev/null
then
    echo "Not logged in to Google Cloud. Please log in:"
    gcloud auth login
fi

# Set the Google Cloud project
echo "Setting Google Cloud project to $PROJECT_ID..."
gcloud config set project $PROJECT_ID

# Export environment variables for deployment
echo "Preparing environment variables for deployment..."
python setup_env.py export --output .env.production

# Build the Docker image
echo "Building Docker image..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

# Deploy to Cloud Run
echo "Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --platform managed \
  --region $REGION \
  --min-instances $MIN_INSTANCES \
  --max-instances $MAX_INSTANCES \
  --memory $MEMORY \
  --cpu $CPU \
  --concurrency $CONCURRENCY \
  --timeout ${TIMEOUT}s \
  --update-env-vars DATABASE_URL="$DATABASE_URL",OPENAI_API_KEY="$OPENAI_API_KEY",ELEVENLABS_API_KEY="$ELEVENLABS_API_KEY",FIREBASE_API_KEY="$FIREBASE_API_KEY",FIREBASE_PROJECT_ID="$FIREBASE_PROJECT_ID",FIREBASE_APP_ID="$FIREBASE_APP_ID",FIREBASE_MEASUREMENT_ID="$FIREBASE_MEASUREMENT_ID",FIREBASE_MESSAGING_SENDER_ID="$FIREBASE_MESSAGING_SENDER_ID",FIREBASE_STORAGE_BUCKET="$FIREBASE_STORAGE_BUCKET",FIREBASE_AUTH_DOMAIN="$FIREBASE_AUTH_DOMAIN",FIREBASE_STORAGE_ENABLED="true" \
  --allow-unauthenticated

# Get the deployed service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format="value(status.url)")

echo "===== Cloud Run Deployment Complete ====="
echo ""
echo "Your application is now available at:"
echo "  - $SERVICE_URL"
echo ""
echo "To set up your custom domain 'childrencastles.com', follow the instructions in:"
echo "CHILDRENCASTLES_DOMAIN_SETUP.md"