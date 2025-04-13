#!/bin/bash
# This script prepares the project for deployment through GitHub Actions

echo "Preparing for GitHub-based deployment..."

# Step 1: Make public directory if it doesn't exist
mkdir -p public

# Step 2: Create a basic package.json in the root directory
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
echo "package.json created"

# Step 3: Create a basic index.js file for Node.js detection
cat > index.js << EOL
// This file is used to ensure buildpack detection for Firebase hosting
console.log('Firebase hosting initialized');
EOL
echo "index.js created"

# Step 4: Create a beautiful landing page in public directory
cat > public/index.html << EOL
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Children's Castle</title>
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
        
        .btn {
            display: inline-block;
            background-color: #4a6da7;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            text-decoration: none;
            margin-top: 20px;
            transition: background-color 0.3s;
        }
        
        .btn:hover {
            background-color: #3a5a8f;
        }
        
        .info {
            margin-top: 30px;
            font-size: 0.9em;
            color: #666;
        }
        
        a {
            color: #4a6da7;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Children's Castle</h1>
        <p>An interactive learning and entertainment platform for children</p>
        
        <div>
            <h2>Welcome to Children's Castle!</h2>
            <p>Your child's adventure into interactive learning and storytelling begins here.</p>
            
            <p>Our application is available at:</p>
            <p><strong>Firebase Hosting:</strong> <a href="https://story-time-fun.web.app" target="_blank">story-time-fun.web.app</a></p>
            <p><strong>Future Domain:</strong> <a href="https://childrencastles.com" target="_blank">childrencastles.com</a> (coming soon)</p>
            
            <a href="/app" class="btn">Enter Children's Castle</a>
        </div>
        
        <div class="info">
            <p>This is our landing page for search engines and informational purposes.</p>
            <p>We're excited for you to experience our interactive stories and games!</p>
        </div>
    </div>
</body>
</html>
EOL
echo "index.html created in public directory"

# Step 5: Create a Firebase configuration file with the correct project ID
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
echo ".firebaserc created"

# Step 6: Create firebase.json configuration
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
echo "firebase.json created"

# Step 7: Create a Firebase test page
cat > public/firebase-config-test.html << EOL
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Firebase Configuration Test</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .success {
            color: green;
            font-weight: bold;
        }
        .error {
            color: red;
            font-weight: bold;
        }
        pre {
            background-color: #f4f4f4;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
        }
    </style>
</head>
<body>
    <h1>Firebase Configuration Test</h1>
    <p>This page tests your Firebase configuration.</p>
    
    <div id="status">Testing Firebase connection...</div>
    <div id="config-display"></div>

    <!-- Firebase App (the core Firebase SDK) -->
    <script src="https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js"></script>
    
    <script>
        // Your Firebase configuration - copied directly from Firebase Console for story-time-fun project
        const firebaseConfig = {
          apiKey: "AIzaSyAPTQO3lnt0GSyDgVCZjtj4i3gk3Qi6Vyo",
          authDomain: "story-time-fun.firebaseapp.com",
          projectId: "story-time-fun",
          storageBucket: "story-time-fun.appspot.com",
          messagingSenderId: "225122848236",
          appId: "1:225122848236:web:5c0cd7632ce0f09973c4c9",
          measurementId: "G-TW65TD3GJ5"
        };
        
        // Display the config (with API key partially hidden)
        const configDisplay = document.getElementById('config-display');
        const displayConfig = {...firebaseConfig};
        if (displayConfig.apiKey) {
            // Only show first and last 4 characters of API key
            const keyLength = displayConfig.apiKey.length;
            displayConfig.apiKey = 
                displayConfig.apiKey.substring(0, 4) + 
                '...' + 
                displayConfig.apiKey.substring(keyLength - 4);
        }
        
        configDisplay.innerHTML = '<h3>Configuration:</h3><pre>' + 
            JSON.stringify(displayConfig, null, 2) + '</pre>';

        // Initialize Firebase
        try {
            const app = firebase.initializeApp(firebaseConfig);
            document.getElementById('status').innerHTML = 
                '<p class="success">Firebase initialized successfully!</p>';
            console.log("Firebase initialized successfully!");
        } catch (error) {
            document.getElementById('status').innerHTML = 
                '<p class="error">Firebase initialization error: ' + error.message + '</p>';
            console.error("Firebase initialization error:", error);
        }
    </script>
</body>
</html>
EOL
echo "Firebase test page created"

echo "GitHub deployment preparation complete!"