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

# Step 2: Run setup to ensure Firebase config is correct
echo "Setting up Firebase configuration..."
chmod +x ./setup_firebase_config.sh
./setup_firebase_config.sh

# Step 3: Log in to Firebase
echo "Please log in to your Firebase account:"
firebase login

# Step 4: Select your Firebase project
echo "Selecting Firebase project..."
firebase use story-time-fun || firebase use --add

# Step 5: Deploy the application
echo "Deploying to Firebase..."
firebase deploy --only hosting

echo "Deployment complete! Your application is now live."
echo "You can access it at https://story-time-fun.web.app"

# Step 6: Remind about custom domain setup
echo
echo "=== CUSTOM DOMAIN REMINDER ==="
echo "If you want to set up your custom domain 'childrencastles.com':"
echo "1. Go to the Firebase Console > Hosting > Add custom domain"
echo "2. Follow the instructions in CUSTOM_DOMAIN_SETUP.md"
echo "3. After setup, your site will be available at https://childrencastles.com"
echo "==========================="