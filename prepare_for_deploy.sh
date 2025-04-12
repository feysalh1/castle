#!/bin/bash
# Script to prepare the Children's Castle application for deployment

echo "===== Preparing Children's Castle for Firebase Hosting ====="

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

# Step 3: Capture live HTML from running application for 1:1 match
echo "Capturing live HTML from the running application..."

# Check if the Flask application is running
if curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/ | grep -q "200"; then
  echo "Flask application is running, capturing live HTML..."
  
  # Make sure we have the required Python packages
  pip install requests beautifulsoup4 >/dev/null 2>&1
  
  # Run the capture script
  python scripts/capture_live_html.py
  
  if [ $? -ne 0 ]; then
    echo "⚠️ Warning: Failed to capture live HTML. Falling back to template HTML creation."
    use_template_html=true
  else
    echo "✅ Successfully captured live HTML from the application!"
    use_template_html=false
    
    # Replace API key placeholders in all HTML files
    echo "Replacing API key placeholders with actual keys..."
    find public -name "*.html" -type f -exec sed -i "s/FIREBASE_API_KEY/$FIREBASE_API_KEY/g" {} \;
    find public -name "*.html" -type f -exec sed -i "s/FIREBASE_APP_ID/$FIREBASE_APP_ID/g" {} \;
    echo "✅ API keys securely injected into HTML files"
  fi
else
  echo "⚠️ Warning: Flask application does not appear to be running. Falling back to template HTML creation."
  use_template_html=true
fi

# If we need to, post-process the images to make them web-friendly
echo "Processing static assets..."
find public -name "*.svg" -type f -size +100k | while read svg_file; do
  echo "  Optimizing large SVG: $svg_file"
  # Use svgo or similar tool if available
  if command -v svgo >/dev/null 2>&1; then
    svgo -q "$svg_file"
  fi
done

# Inject Firebase configuration
echo "Injecting Firebase configuration..."
if command -v sed >/dev/null 2>&1; then
  # Replace FIREBASE_API_KEY and FIREBASE_APP_ID placeholders
  find public -type f -name "*.html" -exec sed -i "s/FIREBASE_API_KEY/$FIREBASE_API_KEY/g" {} \;
  find public -type f -name "*.html" -exec sed -i "s/FIREBASE_APP_ID/$FIREBASE_APP_ID/g" {} \;
  
  # Check if the sed commands succeeded
  if [ $? -ne 0 ]; then
    echo "⚠️ Warning: Could not inject Firebase configuration. Be sure to set the Firebase API key manually."
  else
    echo "✅ Firebase configuration injected successfully!"
  fi
else
  echo "⚠️ Warning: sed command not found. Could not inject Firebase configuration."
  echo "⚠️ This is expected on Windows/Mac as GNU sed may not be available. Firebase functionality may not work correctly."
fi

echo "===== Preparation complete! ====="
echo "The static assets are now prepared for Firebase Hosting."
echo "Run 'firebase deploy --only hosting' to publish the site."
echo "Your site will be available at https://childrencastles.web.app"