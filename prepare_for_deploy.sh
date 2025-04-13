#!/bin/bash
# Script to prepare files for Firebase deployment
# Run this script before deploying to Firebase

# Color output for better readability
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}====================================================${NC}"
echo -e "${BLUE}     Preparing Children's Castle for Deployment     ${NC}"
echo -e "${BLUE}====================================================${NC}"
echo

# 1. Ensure the necessary directories exist
echo -e "${YELLOW}Creating necessary directories...${NC}"
mkdir -p public/js
mkdir -p public/css
mkdir -p public/images

# 2. Copy or create Firebase configuration
echo -e "${YELLOW}Preparing Firebase configuration...${NC}"
# Create a Firebase config file that will be used during deployment
cat > public/js/firebase-config.js << EOL
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
console.log("Firebase initialized with project ID:", firebaseConfig.appId);
console.log("Loading system initialized");
EOL

# 3. Verify config values
echo -e "${YELLOW}Verifying Firebase configuration values...${NC}"
if [ -z "$FIREBASE_API_KEY" ]; then
    echo -e "${RED}ERROR: FIREBASE_API_KEY environment variable is not set${NC}"
    echo -e "${YELLOW}Please ensure your .env file contains a valid FIREBASE_API_KEY${NC}"
    exit 1
fi

if [ -z "$FIREBASE_PROJECT_ID" ]; then
    echo -e "${RED}ERROR: FIREBASE_PROJECT_ID environment variable is not set${NC}"
    echo -e "${YELLOW}Please ensure your .env file contains a valid FIREBASE_PROJECT_ID${NC}"
    exit 1
fi

echo -e "${GREEN}Firebase API Key: Found and valid (first 4 chars: ${FIREBASE_API_KEY:0:4}...)${NC}"
echo -e "${GREEN}Firebase Project ID: $FIREBASE_PROJECT_ID${NC}"

# 4. Create or update .firebaserc
echo -e "${YELLOW}Creating .firebaserc file...${NC}"
cat > .firebaserc << EOL
{
  "projects": {
    "default": "${FIREBASE_PROJECT_ID}"
  },
  "targets": {
    "${FIREBASE_PROJECT_ID}": {
      "hosting": {
        "main": [
          "${FIREBASE_PROJECT_ID}"
        ]
      }
    }
  }
}
EOL

# 5. Make sure our static files are correctly prepared
echo -e "${YELLOW}Preparing static assets for deployment...${NC}"

# 6. Copy robots.txt
echo -e "${YELLOW}Creating robots.txt file...${NC}"
cat > public/robots.txt << EOL
User-agent: *
Allow: /

Sitemap: https://childrencastles.com/sitemap.xml
EOL

# 7. Copy sitemap.xml
echo -e "${YELLOW}Creating sitemap.xml file...${NC}"
cat > public/sitemap.xml << EOL
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://childrencastles.com/</loc>
    <lastmod>$(date +%Y-%m-%d)</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://childrencastles.com/app</loc>
    <lastmod>$(date +%Y-%m-%d)</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
</urlset>
EOL

echo -e "${GREEN}====================================================${NC}"
echo -e "${GREEN}       Deployment Preparation Complete!             ${NC}"
echo -e "${GREEN}====================================================${NC}"
echo -e "${BLUE}You can now run ./deploy.sh to deploy to Firebase${NC}"
echo