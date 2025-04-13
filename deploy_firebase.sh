#!/bin/bash
# This script handles Firebase deployment

# Set error handling
set -e

echo "=== Children's Castle Firebase Deployment ==="
echo "Deploying to Firebase project: story-time-fun"

# Make sure the public directory exists
if [ ! -d "public" ]; then
  echo "Creating public directory..."
  mkdir -p public
fi

# Make sure there's an index.html file
if [ ! -f "public/index.html" ]; then
  echo "Creating basic index.html..."
  cat > public/index.html << EOL
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Children's Castle</title>
  <meta http-equiv="refresh" content="0;URL='/'" />
</head>
<body>
  <p>Redirecting to application...</p>
  <script>window.location.href = '/';</script>
</body>
</html>
EOL
fi

# Create a simpler firebase.json for direct hosting
echo "Creating simplified firebase.json..."
cat > firebase.json << EOL
{
  "hosting": {
    "site": "story-time-fun",
    "public": "public",
    "ignore": [
      "firebase.json",
      "**/.*",
      "**/node_modules/**"
    ]
  }
}
EOL

# Run the deploy command
echo "Deploying to Firebase..."
firebase deploy --only hosting --project story-time-fun

echo "=== Deployment completed ==="
echo "Your site should be available at: https://story-time-fun.web.app"