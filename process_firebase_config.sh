#!/bin/bash
# This script processes the Firebase configuration file and replaces placeholders with actual values

# Ensure the directory exists
mkdir -p public/js

# Copy the template
cp static/js/firebase-config.js public/js/firebase-config.js

# Replace placeholders with actual values
sed -i "s|\${FIREBASE_API_KEY}|$FIREBASE_API_KEY|g" public/js/firebase-config.js
sed -i "s|\${FIREBASE_AUTH_DOMAIN}|$FIREBASE_AUTH_DOMAIN|g" public/js/firebase-config.js
sed -i "s|\${FIREBASE_PROJECT_ID}|$FIREBASE_PROJECT_ID|g" public/js/firebase-config.js
sed -i "s|\${FIREBASE_STORAGE_BUCKET}|$FIREBASE_STORAGE_BUCKET|g" public/js/firebase-config.js
sed -i "s|\${FIREBASE_MESSAGING_SENDER_ID}|$FIREBASE_MESSAGING_SENDER_ID|g" public/js/firebase-config.js
sed -i "s|\${FIREBASE_APP_ID}|$FIREBASE_APP_ID|g" public/js/firebase-config.js
sed -i "s|\${FIREBASE_MEASUREMENT_ID}|$FIREBASE_MEASUREMENT_ID|g" public/js/firebase-config.js

echo "Firebase configuration processed for deployment"