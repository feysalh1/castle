#!/bin/bash

# Deploy the application to Firebase Hosting
# This script should be run after the application is ready for deployment

echo "===== Starting Firebase Deployment ====="
echo "Deploying to project: story-time-fun"

# Check if firebase CLI is available
if ! command -v firebase &> /dev/null
then
    echo "Firebase CLI is not installed. Installing..."
    npm install -g firebase-tools
fi

# Check if user is logged in to Firebase
if ! firebase projects:list &> /dev/null
then
    echo "Not logged in to Firebase. Please log in:"
    firebase login
fi

# Export Firebase configuration to the public directory
echo "Exporting Firebase configuration..."
python setup_env.py firebase-json --output public/firebase-config.js

# Update Firebase configuration from environment
echo "Updating Firebase configuration in public directory..."
sed -i 's/{/{const firebaseConfig = {/g' public/firebase-config.js
echo "};

// Initialize Firebase
try {
  const app = firebase.initializeApp(firebaseConfig);
  console.log('Firebase initialized successfully in static hosting');
} catch (e) {
  console.error('Firebase initialization error:', e);
}" >> public/firebase-config.js

# Deploy to Firebase Hosting
echo "Deploying to Firebase Hosting..."
firebase deploy --only hosting

echo "===== Firebase Deployment Complete ====="
echo ""
echo "Your application is now available at:"
echo "  - https://story-time-fun.web.app"
echo "  - https://story-time-fun.firebaseapp.com"
echo ""
echo "To set up your custom domain 'childrencastles.com', follow the instructions in:"
echo "CHILDRENCASTLES_DOMAIN_SETUP.md"