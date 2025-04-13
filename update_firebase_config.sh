#!/bin/bash
# Script to update Firebase configuration across all relevant files
# Usage: ./update_firebase_config.sh "your-api-key" "your-project-id"

# Check if arguments are provided
if [ "$#" -lt 1 ]; then
    echo "Usage: ./update_firebase_config.sh \"your-api-key\" [\"your-project-id\"]"
    echo "  - your-api-key: The Firebase API key for the project"
    echo "  - your-project-id: (Optional) The Firebase project ID (defaults to story-time-fun)"
    exit 1
fi

# Set variables
API_KEY=$1
PROJECT_ID=${2:-"story-time-fun"}
AUTH_DOMAIN="${PROJECT_ID}.firebaseapp.com"
STORAGE_BUCKET="${PROJECT_ID}.appspot.com"

echo "Updating Firebase configuration with:"
echo "API KEY: ${API_KEY:0:4}...${API_KEY: -4}" # Show first and last 4 characters only
echo "PROJECT ID: $PROJECT_ID"

# 1. Update .firebaserc file
echo "Updating .firebaserc..."
cat > .firebaserc << EOL
{
  "projects": {
    "default": "${PROJECT_ID}"
  },
  "targets": {
    "${PROJECT_ID}": {
      "hosting": {
        "main": [
          "${PROJECT_ID}"
        ]
      }
    }
  }
}
EOL

# 2. Update Firebase test page
echo "Updating Firebase test page..."
sed -i "s/apiKey: \"[^\"]*\"/apiKey: \"${API_KEY}\"/g" public/firebase-config-test.html
sed -i "s/projectId: \"[^\"]*\"/projectId: \"${PROJECT_ID}\"/g" public/firebase-config-test.html
sed -i "s/authDomain: \"[^\"]*\"/authDomain: \"${AUTH_DOMAIN}\"/g" public/firebase-config-test.html
sed -i "s/storageBucket: \"[^\"]*\"/storageBucket: \"${STORAGE_BUCKET}\"/g" public/firebase-config-test.html

# 3. Update GitHub workflow files
echo "Updating GitHub workflow files..."
sed -i "s/projectId: [^\n]*/projectId: ${PROJECT_ID}/g" .github/workflows/firebase-deploy.yml
sed -i "s/firebaseHostingSite: [^\n]*/firebaseHostingSite: ${PROJECT_ID}/g" .github/workflows/firebase-deploy.yml

# 4. Update prepare_github_deploy.sh to use the correct configuration
echo "Updating prepare_github_deploy.sh..."
sed -i "s/apiKey: \"[^\"]*\"/apiKey: \"${API_KEY}\"/g" prepare_github_deploy.sh
sed -i "s/projectId: \"[^\"]*\"/projectId: \"${PROJECT_ID}\"/g" prepare_github_deploy.sh
sed -i "s/authDomain: \"[^\"]*\"/authDomain: \"${AUTH_DOMAIN}\"/g" prepare_github_deploy.sh
sed -i "s/storageBucket: \"[^\"]*\"/storageBucket: \"${STORAGE_BUCKET}\"/g" prepare_github_deploy.sh

# 5. Update firebase.json if needed
echo "Checking firebase.json..."
if grep -q "\"site\": \"" firebase.json; then
    sed -i "s/\"site\": \"[^\"]*\"/\"site\": \"${PROJECT_ID}\"/g" firebase.json
    echo "Updated site in firebase.json"
fi

# 6. Update environment variables
if [ -f ".env" ]; then
    echo "Updating .env file..."
    # Check if FIREBASE_API_KEY exists in .env
    if grep -q "FIREBASE_API_KEY=" .env; then
        sed -i "s/FIREBASE_API_KEY=.*/FIREBASE_API_KEY=${API_KEY}/g" .env
    else
        echo "FIREBASE_API_KEY=${API_KEY}" >> .env
    fi
    
    # Check if FIREBASE_PROJECT_ID exists in .env
    if grep -q "FIREBASE_PROJECT_ID=" .env; then
        sed -i "s/FIREBASE_PROJECT_ID=.*/FIREBASE_PROJECT_ID=${PROJECT_ID}/g" .env
    else
        echo "FIREBASE_PROJECT_ID=${PROJECT_ID}" >> .env
    fi
    
    # Update other Firebase-related environment variables
    if grep -q "FIREBASE_AUTH_DOMAIN=" .env; then
        sed -i "s/FIREBASE_AUTH_DOMAIN=.*/FIREBASE_AUTH_DOMAIN=${AUTH_DOMAIN}/g" .env
    else
        echo "FIREBASE_AUTH_DOMAIN=${AUTH_DOMAIN}" >> .env
    fi
    
    if grep -q "FIREBASE_STORAGE_BUCKET=" .env; then
        sed -i "s/FIREBASE_STORAGE_BUCKET=.*/FIREBASE_STORAGE_BUCKET=${STORAGE_BUCKET}/g" .env
    else
        echo "FIREBASE_STORAGE_BUCKET=${STORAGE_BUCKET}" >> .env
    fi
else
    echo "No .env file found. Creating one with Firebase configuration..."
    cat > .env << EOL
FIREBASE_API_KEY=${API_KEY}
FIREBASE_PROJECT_ID=${PROJECT_ID}
FIREBASE_AUTH_DOMAIN=${AUTH_DOMAIN}
FIREBASE_STORAGE_BUCKET=${STORAGE_BUCKET}
EOL
fi

echo "Firebase configuration updated successfully!"
echo ""
echo "Next steps:"
echo "1. Test your configuration with ./deploy.sh"
echo "2. Or check the setup with ./test_firebase_connection.sh"
echo "3. Access the test page at /firebase-config-test.html in your browser"