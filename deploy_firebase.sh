#!/bin/bash

# Deploy Firebase-specific components for Children's Castle

echo "Starting Firebase deployment for Children's Castle..."

# Check if Firebase CLI is installed
if ! command -v firebase &> /dev/null; then
    echo "Firebase CLI not found. Installing..."
    npm install -g firebase-tools
fi

# Make sure we're logged in
echo "Checking Firebase login status..."
firebase login:list

# Check for the presence of firebase-config.js
if [ ! -f "public/firebase-config.js" ]; then
    echo "ERROR: public/firebase-config.js not found."
    echo "Please create this file with your Firebase configuration."
    exit 1
fi

# Check for firebase.json
if [ ! -f "firebase.json" ]; then
    echo "ERROR: firebase.json not found."
    echo "Please create a Firebase configuration file."
    exit 1
fi

# Optional: Create a 404 page if not exists
if [ ! -f "public/404.html" ]; then
    echo "Creating a simple 404 page..."
    cat > public/404.html << EOF
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Page Not Found - Children's Castle</title>
    <link rel="stylesheet" href="/css/main.css">
    <style>
        .container { text-align: center; padding: 40px; }
        h1 { margin-bottom: 20px; }
        .back-link { margin-top: 30px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Page Not Found</h1>
        <p>The page you requested could not be found.</p>
        <div class="back-link">
            <a href="/" class="btn">Go back to home page</a>
        </div>
    </div>
</body>
</html>
EOF
fi

# Deploy to Firebase
echo "Deploying to Firebase Hosting..."
firebase deploy --only hosting

echo "Firebase deployment completed."
echo "Your app should be available at: https://story-time-fun.web.app"
echo ""
echo "Next steps:"
echo "1. Configure custom domain in Firebase console"
echo "2. Deploy backend to Cloud Run with: ./deploy_to_cloud_run.sh"
echo "3. Update Firebase rewrites if needed for the Cloud Run service"