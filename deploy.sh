#!/bin/bash
# Script to deploy Children's Castle to Firebase Hosting
# This script handles the entire deployment process

# Color output for better readability
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}====================================================${NC}"
echo -e "${BLUE}       Deploying Children's Castle to Firebase      ${NC}"
echo -e "${BLUE}====================================================${NC}"
echo

# Step 1: Check if Firebase CLI is installed
echo -e "${YELLOW}Checking for Firebase CLI...${NC}"
if ! command -v firebase &> /dev/null; then
    echo -e "${RED}Firebase CLI not found. Installing...${NC}"
    npm install -g firebase-tools
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to install Firebase CLI. Please install it manually:${NC}"
        echo -e "${YELLOW}npm install -g firebase-tools${NC}"
        exit 1
    fi
fi
echo -e "${GREEN}Firebase CLI is installed.${NC}"

# Step 2: Run the preparation script
echo -e "${YELLOW}Running preparation script...${NC}"
chmod +x ./prepare_for_deploy.sh
./prepare_for_deploy.sh

if [ $? -ne 0 ]; then
    echo -e "${RED}Preparation script failed. Aborting deployment.${NC}"
    exit 1
fi

# Step 3: Make sure the public directory has the necessary files
echo -e "${YELLOW}Checking for required files...${NC}"
if [ ! -f "public/index-firebase.html" ]; then
    echo -e "${RED}Error: public/index-firebase.html not found${NC}"
    echo -e "${YELLOW}Creating a simple redirect page...${NC}"
    
    # Create a simple redirect page
    mkdir -p public
    cat > public/index-firebase.html << EOL
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Children's Castle - Redirecting...</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background-color: #f0f8ff;
            color: #333;
        }
        
        .container {
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            padding: 30px;
            width: 90%;
            max-width: 600px;
            text-align: center;
        }
        
        h1 {
            color: #4a6da7;
            margin-bottom: 10px;
        }
        
        p {
            margin: 15px 0;
            line-height: 1.5;
        }
        
        .loading {
            margin: 20px auto;
            width: 50px;
            height: 50px;
            border: 5px solid #f0f8ff;
            border-top: 5px solid #4a6da7;
            border-radius: 50%;
            animation: spin 2s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Children's Castle</h1>
        <p>Welcome to Children's Castle! The application is loading...</p>
        <div class="loading"></div>
        <p>If you are not redirected automatically, please <a href="/app">click here</a>.</p>
    </div>

    <script>
        // Redirect to app after a short delay
        setTimeout(function() {
            window.location.href = "/app";
        }, 2000);
    </script>
</body>
</html>
EOL
fi

echo -e "${GREEN}Required files are present.${NC}"

# Step 4: Check Firebase login status
echo -e "${YELLOW}Checking Firebase login status...${NC}"
firebase login:list &> /dev/null

if [ $? -ne 0 ]; then
    echo -e "${YELLOW}You are not logged in to Firebase. Please log in:${NC}"
    firebase login
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to log in to Firebase. Aborting deployment.${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}Firebase login confirmed.${NC}"

# Step 5: Deploy to Firebase Hosting
echo -e "${YELLOW}Deploying to Firebase Hosting...${NC}"
firebase deploy --only hosting

if [ $? -ne 0 ]; then
    echo -e "${RED}Deployment failed. Please check the error messages above.${NC}"
    exit 1
fi

# Step 6: Display success message with the URLs
echo -e "${GREEN}====================================================${NC}"
echo -e "${GREEN}       Deployment Completed Successfully!           ${NC}"
echo -e "${GREEN}====================================================${NC}"
echo -e "${BLUE}Your site is now live at:${NC}"
echo -e "${YELLOW}https://${FIREBASE_PROJECT_ID}.web.app${NC}"
echo -e "${YELLOW}https://${FIREBASE_PROJECT_ID}.firebaseapp.com${NC}"
echo
echo -e "${BLUE}If you've set up a custom domain, your site will also be available at:${NC}"
echo -e "${YELLOW}https://childrencastles.com${NC} (Once DNS propagation is complete)"
echo
echo -e "${BLUE}To set up a custom domain, follow the instructions in:${NC}"
echo -e "${YELLOW}CUSTOM_DOMAIN_SETUP.md${NC}"