#!/bin/bash
# Script to prepare the Children's Castle application for GitHub Actions deployment to Firebase

echo "===== Preparing Children's Castle for GitHub Actions Deployment ====="

# Step 1: Create directory structure
echo "Creating public directory structure..."
rm -rf public
mkdir -p public
mkdir -p public/css
mkdir -p public/js
mkdir -p public/images
mkdir -p public/audio
mkdir -p public/data

# Step 2: Copy static files
echo "Copying static files..."
cp -r static/* public/

# Step 3: Create an index.html that redirects to the backend
echo "Creating index.html with redirect to backend service..."
cat > public/index.html << EOL
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Children's Castle</title>
  <meta http-equiv="refresh" content="0;URL='https://childrenscastle-backend.run.app/'" />
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 20px;
      text-align: center;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100vh;
      background-color: #f0f9ff;
    }
    .loader {
      border: 16px solid #f3f3f3;
      border-radius: 50%;
      border-top: 16px solid #3498db;
      width: 120px;
      height: 120px;
      animation: spin 2s linear infinite;
      margin-bottom: 20px;
    }
    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
  </style>
</head>
<body>
  <div class="loader"></div>
  <h1>Redirecting to Children's Castle</h1>
  <p>If you are not redirected automatically, follow this <a href="https://childrenscastle-backend.run.app/">link</a>.</p>
  <script>
    window.location.href = 'https://childrenscastle-backend.run.app/';
  </script>
</body>
</html>
EOL

# Step 4: Copy templates 
echo "Copying template files (for future static usage)..."
cp -r templates public/templates

echo "===== Preparation complete! ====="
echo "The static assets are now prepared for GitHub Actions deployment to Firebase Hosting."
echo "Your site will be available at https://childrencastles.web.app"
echo "and at your custom domain: https://childrencastles.com if configured"