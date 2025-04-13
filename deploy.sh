#!/bin/bash
# Enhanced Deployment script for Children's Castle application

# Make script executable with: chmod +x deploy.sh
# Run with: ./deploy.sh

# Set variables for better error handling
set -e  # Exit on any error
FIREBASE_PROJECT="story-time-fun"

# Color output for better readability
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Show header
echo -e "${BLUE}====================================================${NC}"
echo -e "${BLUE}       Children's Castle Deployment Script          ${NC}"
echo -e "${BLUE}====================================================${NC}"
echo

# Step 1: Verify environment variables
echo -e "${YELLOW}Step 1: Verifying Firebase environment variables...${NC}"
if [ -z "$FIREBASE_API_KEY" ]; then
    echo -e "${RED}Error: FIREBASE_API_KEY is not set in environment variables.${NC}"
    echo -e "Please check your .env file and make sure it's being loaded properly."
    exit 1
fi

if [ -z "$FIREBASE_PROJECT_ID" ]; then
    echo -e "${YELLOW}Warning: FIREBASE_PROJECT_ID not found in environment. Using default: $FIREBASE_PROJECT${NC}"
else
    FIREBASE_PROJECT="$FIREBASE_PROJECT_ID"
    echo -e "${GREEN}Using Firebase project ID from environment: $FIREBASE_PROJECT${NC}"
fi

echo -e "${GREEN}Environment variables verified!${NC}"
echo

# Step 2: Ensure Firebase tools are installed
echo -e "${YELLOW}Step 2: Checking Firebase tools...${NC}"
if ! command -v firebase &> /dev/null; then
    echo -e "${BLUE}Firebase CLI not found. Installing...${NC}"
    npm install -g firebase-tools
else
    echo -e "${GREEN}Firebase CLI is already installed.${NC}"
fi
echo

# Step 3: Make sure .firebaserc exists with correct project
echo -e "${YELLOW}Step 3: Configuring Firebase project...${NC}"
cat > .firebaserc << EOL
{
  "projects": {
    "default": "${FIREBASE_PROJECT}"
  },
  "targets": {
    "${FIREBASE_PROJECT}": {
      "hosting": {
        "main": [
          "${FIREBASE_PROJECT}"
        ]
      }
    }
  }
}
EOL
echo -e "${GREEN}.firebaserc file created/updated with project: ${FIREBASE_PROJECT}${NC}"
echo

# Step 4: Create a public/404.html file to handle missing routes
echo -e "${YELLOW}Step 4: Setting up 404 page...${NC}"
if [ ! -f "public/404.html" ]; then
    cat > public/404.html << EOL
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Page Not Found | Children's Castle</title>
    <style>
      body { 
        font-family: 'Arial', sans-serif; 
        text-align: center; 
        padding: 40px;
        background-color: #f0f8ff;
      }
      h1 { color: #4a6da7; }
      .container {
        max-width: 600px;
        margin: 0 auto;
        background: white;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
      }
      .btn {
        display: inline-block;
        background-color: #4a6da7;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        text-decoration: none;
        margin-top: 20px;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>Page Not Found</h1>
      <p>The page you're looking for doesn't exist.</p>
      <a href="/" class="btn">Return to Home</a>
    </div>

    <script>
      // Redirect to the home page for SPA routing
      document.addEventListener('DOMContentLoaded', function() {
        // You might want to send to the main app
        // window.location.href = '/';
      });
    </script>
  </body>
</html>
EOL
    echo -e "${GREEN}404 page created!${NC}"
else
    echo -e "${GREEN}404 page already exists.${NC}"
fi
echo

# Step 5: Login to Firebase
echo -e "${YELLOW}Step 5: Logging in to Firebase...${NC}"
firebase login
echo

# Step 6: Make sure we're using the right project
echo -e "${YELLOW}Step 6: Setting active Firebase project...${NC}"
firebase use "$FIREBASE_PROJECT" || firebase use --add
echo

# Step 7: Process Firebase configuration
echo -e "${YELLOW}Step 7: Processing Firebase configuration...${NC}"
chmod +x ./process_firebase_config.sh
./process_firebase_config.sh
echo -e "${GREEN}Firebase configuration processed.${NC}"
echo

# Step 8: Deploy the application
echo -e "${YELLOW}Step 8: Deploying to Firebase Hosting...${NC}"
firebase deploy --only hosting
echo

# Step 8: Success message
echo -e "${GREEN}==================================================${NC}"
echo -e "${GREEN} Deployment complete! Your application is now live.${NC}"
echo -e "${GREEN} You can access it at:${NC}"
echo -e "${BLUE} https://${FIREBASE_PROJECT}.web.app${NC}"
echo
echo -e "${YELLOW}=== CUSTOM DOMAIN REMINDER ===${NC}"
echo -e "${YELLOW}If you want to set up your custom domain 'childrencastles.com':${NC}"
echo -e "${YELLOW}1. Go to the Firebase Console > Hosting > Add custom domain${NC}"
echo -e "${YELLOW}2. Follow the instructions in CUSTOM_DOMAIN_SETUP.md${NC}"
echo -e "${YELLOW}3. After setup, your site will be available at https://childrencastles.com${NC}"
echo -e "${GREEN}==================================================${NC}"