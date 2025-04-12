#!/bin/bash
# Deploy Children's Castle to Cloud Run and Firebase
# This script requires gcloud and firebase CLI tools to be installed

set -e  # Exit on any error

echo "===== Deploying Children's Castle to Cloud Run and Firebase ====="

# Check if user is logged in to gcloud
echo "Checking Google Cloud authentication..."
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" 2>/dev/null | grep -q "@"; then
    echo "You need to log in to Google Cloud first."
    gcloud auth login
fi

# Check if Firebase CLI is available
if ! command -v firebase &> /dev/null; then
    echo "Firebase CLI not found. Please install it with 'npm install -g firebase-tools'"
    exit 1
fi

# Get the Google Cloud project ID
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
if [ -z "$PROJECT_ID" ]; then
    echo "No Google Cloud project selected. Please select one:"
    gcloud projects list
    echo -n "Enter the project ID: "
    read PROJECT_ID
    gcloud config set project "$PROJECT_ID"
fi

echo "Using Google Cloud project: $PROJECT_ID"

# Collect environment variables
echo "Please provide the necessary environment variables:"

echo -n "DATABASE_URL: "
read DATABASE_URL

echo -n "OPENAI_API_KEY: "
read OPENAI_API_KEY

echo -n "FIREBASE_API_KEY: "
read FIREBASE_API_KEY

echo -n "FIREBASE_APP_ID: "
read FIREBASE_APP_ID

echo -n "ELEVENLABS_API_KEY: "
read ELEVENLABS_API_KEY

# Update cloudbuild.yaml with the correct environment variables
echo "Updating cloudbuild.yaml with environment variables..."
sed -i.bak \
    -e "s|_DATABASE_URL: ''|_DATABASE_URL: '$DATABASE_URL'|g" \
    -e "s|_OPENAI_API_KEY: ''|_OPENAI_API_KEY: '$OPENAI_API_KEY'|g" \
    -e "s|_FIREBASE_API_KEY: ''|_FIREBASE_API_KEY: '$FIREBASE_API_KEY'|g" \
    -e "s|_FIREBASE_PROJECT_ID: 'story-time-fun'|_FIREBASE_PROJECT_ID: '$PROJECT_ID'|g" \
    -e "s|_FIREBASE_APP_ID: ''|_FIREBASE_APP_ID: '$FIREBASE_APP_ID'|g" \
    -e "s|_ELEVENLABS_API_KEY: ''|_ELEVENLABS_API_KEY: '$ELEVENLABS_API_KEY'|g" \
    cloudbuild.yaml

# Update firebase.json to use the correct project and region
echo "Updating firebase.json to use the correct project and region..."
sed -i.bak \
    -e "s|\"serviceId\": \"childrens-castle\"|\"serviceId\": \"childrens-castle\"|g" \
    -e "s|\"region\": \"us-central1\"|\"region\": \"us-central1\"|g" \
    firebase.json

# Update .firebaserc with the correct project
echo "Updating .firebaserc with the correct project ID..."
cat > .firebaserc << EOL
{
  "projects": {
    "default": "${PROJECT_ID}"
  }
}
EOL

# Enable required APIs
echo "Enabling required Google Cloud APIs..."
gcloud services enable \
    cloudbuild.googleapis.com \
    run.googleapis.com \
    containerregistry.googleapis.com \
    firebasehosting.googleapis.com

# Build and deploy to Cloud Run using Cloud Build
echo "Submitting build to Cloud Build..."
gcloud builds submit

# Wait for deployment to complete
echo "Waiting for Cloud Run deployment to complete..."
sleep 10  # Give it some time to start

# Check that the service is deployed
CLOUD_RUN_URL=$(gcloud run services describe childrens-castle --platform managed --region us-central1 --format="value(status.url)" 2>/dev/null || echo "")
if [ -z "$CLOUD_RUN_URL" ]; then
    echo "Cloud Run deployment may have failed. Please check the Cloud Console."
    exit 1
fi

echo "Cloud Run service deployed at: $CLOUD_RUN_URL"

# Deploy to Firebase Hosting
echo "Deploying to Firebase Hosting..."
firebase deploy --only hosting

echo "===== Deployment Complete! ====="
echo "Your application is now available at:"
echo "- Cloud Run: $CLOUD_RUN_URL"
echo "- Firebase: https://$PROJECT_ID.web.app"
echo ""
echo "To set up a custom domain, use the Firebase console."