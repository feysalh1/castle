#!/bin/bash
# This script prepares the project for deployment through GitHub Actions

# Make public directory if it doesn't exist
mkdir -p public

# Create a basic package.json in the root directory to trigger Node.js detection
cat > package.json << EOL
{
  "name": "childrens-castle",
  "version": "1.0.0",
  "description": "Children's Castle interactive storytelling application",
  "main": "index.js",
  "scripts": {
    "build": "echo 'Static hosting only, no build required'",
    "test": "echo 'No tests defined'"
  },
  "engines": {
    "node": "18.x"
  },
  "dependencies": {
    "firebase": "^11.0.0",
    "firebase-admin": "^11.0.0",
    "firebase-functions": "^4.0.0"
  }
}
EOL

# Create a basic index.js file to help with Node.js detection
cat > index.js << EOL
// This file is used to ensure buildpack detection for Firebase hosting
console.log('Firebase hosting initialized');
EOL

# Create a placeholder index.html in public directory if it doesn't exist
if [ ! -f public/index.html ]; then
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
  <script>
    window.location.href = '/';
  </script>
</body>
</html>
EOL
fi

# Create a .firebaserc file if it doesn't exist
if [ ! -f .firebaserc ]; then
  cat > .firebaserc << EOL
{
  "projects": {
    "default": "story-time-fun"
  }
}
EOL
fi

echo "Deployment preparation complete!"