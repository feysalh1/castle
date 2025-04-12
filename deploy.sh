#!/bin/bash
# Deployment script for Children's Castle application

# Make script executable with: chmod +x deploy.sh
# Run with: ./deploy.sh

echo "Starting deployment process for Children's Castle..."

# Step 1: Ensure Firebase is installed
if ! command -v firebase &> /dev/null; then
    echo "Firebase CLI not found. Installing..."
    npm install -g firebase-tools
fi

# Step 2: Log in to Firebase
echo "Please log in to your Firebase account:"
firebase login

# Step 3: Select your Firebase project
echo "Selecting Firebase project..."
firebase use childrens-castle || firebase use --add

# Step 4: Deploy the application
echo "Deploying to Firebase..."
firebase deploy --only hosting

echo "Deployment complete! Your application is now live."
echo "You can access it at https://childrens-castle.web.app"