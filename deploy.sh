#!/bin/bash

# Combined deployment script for Children's Castle application
# This script deploys both the backend to Cloud Run and the static content to Firebase Hosting

echo "===== Children's Castle Full Deployment Process ====="
echo "This script will deploy your application to:"
echo "1. Google Cloud Run (backend service)"
echo "2. Firebase Hosting (frontend/static content)"
echo ""
echo "Project: story-time-fun"

# Check the requirements
echo "Checking deployment requirements..."

# Check if required tools are installed
if ! command -v gcloud &> /dev/null
then
    echo "Google Cloud SDK not found. Please install it first."
    exit 1
fi

if ! command -v firebase &> /dev/null
then
    echo "Firebase CLI not found. Installing..."
    npm install -g firebase-tools
fi

if ! command -v python &> /dev/null
then
    echo "Python not found. Please install Python 3.8+ first."
    exit 1
fi

# Check if python-dotenv is installed
if ! python -c "import dotenv" &> /dev/null
then
    echo "Installing python-dotenv package for environment variable management..."
    pip install python-dotenv
fi

# Check authentication
echo "Checking Google Cloud authentication..."
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" &> /dev/null
then
    echo "Not logged in to Google Cloud. Please log in:"
    gcloud auth login
fi

echo "Checking Firebase authentication..."
if ! firebase projects:list &> /dev/null
then
    echo "Not logged in to Firebase. Please log in:"
    firebase login
fi

# Environment setup
echo "Setting up environment for deployment..."
echo "Verifying .env file and environment variables..."

# Make the environment setup script executable
chmod +x setup_env.py

# Verify environment variables
python setup_env.py setup

# Deploy to Cloud Run first
echo ""
echo "===== Step 1: Deploying backend to Google Cloud Run ====="
bash ./deploy_to_cloud_run.sh

# Deploy to Firebase Hosting
echo ""
echo "===== Step 2: Deploying frontend to Firebase Hosting ====="
bash ./deploy_firebase.sh

# Final instructions
echo ""
echo "===== Deployment Complete! ====="
echo ""
echo "Your application is now available at:"
echo "  - https://story-time-fun.web.app (Firebase Hosting)"
echo "  - https://childrens-castle-xxxxx.run.app (Cloud Run)"
echo ""
echo "For custom domain setup instructions, see:"
echo "CHILDRENCASTLES_DOMAIN_SETUP.md"
echo ""
echo "Important Next Steps:"
echo "1. Connect your Firebase Hosting to the Cloud Run backend"
echo "2. Set up your custom domain 'childrencastles.com'"
echo "3. Test your application thoroughly"
echo ""
echo "Thank you for using Children's Castle! 🏰"