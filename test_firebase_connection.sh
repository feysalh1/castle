#!/bin/bash
# Test Firebase connection and configuration for storytimefun project

echo "Testing Firebase connection for story-time-fun project..."

# Check if firebase CLI is installed
if ! command -v firebase &> /dev/null; then
    echo "Firebase CLI not found. Installing..."
    npm install -g firebase-tools
fi

# Check if logged in to Firebase
echo "Checking Firebase login status..."
firebase login:list

# Verify project ID
echo "Verifying Firebase project configuration..."
firebase projects:list | grep story-time-fun

# Check our current .firebaserc configuration
echo "Current .firebaserc configuration:"
cat .firebaserc

# Test the hosting configuration
echo "Testing Firebase hosting configuration..."
firebase hosting:sites --project story-time-fun

echo "Firebase configuration test complete."
echo "If you don't see the project 'story-time-fun' listed above, please run:"
echo "firebase login"
echo "firebase use story-time-fun"