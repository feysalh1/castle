#!/bin/bash
# Setup Firebase Configuration for Children's Castle

# Check if we need to regenerate the .firebaserc file
echo "Setting up Firebase configuration..."

# Create .firebaserc file
cat > .firebaserc << EOL
{
  "projects": {
    "default": "story-time-fun"
  },
  "targets": {
    "story-time-fun": {
      "hosting": {
        "main": [
          "story-time-fun"
        ]
      }
    }
  }
}
EOL
echo ".firebaserc file created"

# Create firebase.json file
cat > firebase.json << EOL
{
  "hosting": {
    "public": "public",
    "ignore": [
      "firebase.json",
      "**/.*",
      "**/node_modules/**"
    ],
    "rewrites": [
      {
        "source": "**",
        "destination": "/index.html"
      }
    ]
  }
}
EOL
echo "firebase.json file created"

# Create a JavaScript config file for client-side Firebase usage
mkdir -p static/js
cat > static/js/firebase-config.js << EOL
// Firebase configuration for Children's Castle
const firebaseConfig = {
  apiKey: "${FIREBASE_API_KEY}",
  authDomain: "${FIREBASE_AUTH_DOMAIN}",
  projectId: "${FIREBASE_PROJECT_ID}",
  storageBucket: "${FIREBASE_STORAGE_BUCKET}",
  messagingSenderId: "${FIREBASE_MESSAGING_SENDER_ID}",
  appId: "${FIREBASE_APP_ID}",
  measurementId: "${FIREBASE_MEASUREMENT_ID}"
};

// Initialize Firebase
const app = firebase.initializeApp(firebaseConfig);
EOL
echo "Firebase client-side configuration created"

# Create an inline test page for Firebase
cat > public/firebase-inline-test.html << EOL
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Firebase Config Test</title>
</head>
<body>
    <h1>Firebase Configuration Test</h1>
    <p>This page tests your Firebase configuration directly.</p>
    <div id="status">Testing Firebase connection...</div>

    <!-- Firebase JS SDKs -->
    <script src="https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js"></script>
    <script src="https://www.gstatic.com/firebasejs/10.7.1/firebase-analytics.js"></script>

    <script>
      // This script automatically loads the environment variables from your Firebase project
      fetch('/firebase-config.json')
        .then(response => response.json())
        .then(config => {
          // Initialize Firebase with fetched config
          const app = firebase.initializeApp(config);
          document.getElementById('status').innerHTML = 'Firebase initialized successfully!';
        })
        .catch(error => {
          document.getElementById('status').innerHTML = 'Error loading Firebase config: ' + error.message;
        });
    </script>
</body>
</html>
EOL
echo "Firebase inline test page created"

echo "Firebase configuration setup complete!"