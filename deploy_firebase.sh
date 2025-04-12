#!/bin/bash
# Firebase deployment script using CI token

# Display banner
echo "=================================================="
echo "    Children's Castle Firebase Deployment Tool    "
echo "=================================================="
echo

# Check if token is set
if [ -z "$FIREBASE_TOKEN" ]; then
  echo "❌ Error: FIREBASE_TOKEN is not set."
  echo "Please add your Firebase token as a secret in Replit:"
  echo "1. Go to Tools > Secrets"
  echo "2. Add a new secret with key FIREBASE_TOKEN"
  echo "3. Set the value to your Firebase CI token"
  echo "4. Restart the Replit environment"
  echo
  echo "To generate a token, run 'firebase login:ci' on your local machine."
  exit 1
fi

# Run deployment script
echo "📤 Deploying to Firebase Hosting..."
echo

# First run prepare script
echo "🔧 Preparing for deployment..."
bash ./prepare_for_deploy.sh

# Deploy to Firebase
echo
echo "🚀 Deploying to Firebase Hosting..."
firebase deploy --token "$FIREBASE_TOKEN" --only hosting

# Check deployment status
if [ $? -eq 0 ]; then
  echo
  echo "✅ Deployment successful!"
  echo "Your site should be available at:"
  echo "https://childrens-castle.web.app"
else
  echo
  echo "❌ Deployment failed. Please check the error messages above."
fi