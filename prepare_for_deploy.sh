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

# Step 2: Copy static files
echo "Copying static files..."
cp -r static/* public/
cp -r static/css/* public/css/
cp -r static/js/* public/js/
cp -r static/images/* public/images/

# Step 3: Create sample index page for hosting
echo "Creating main index.html..."
cat > public/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Children's Castle - Interactive Storytime</title>
  <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700&display=swap" rel="stylesheet">
  <link href="/css/style.css" rel="stylesheet">
  <link href="/css/story-mode.css" rel="stylesheet">
  <link href="/css/game-mode.css" rel="stylesheet">
  <link href="/css/shooting-star.css" rel="stylesheet">
  <style>
    body {
      font-family: 'Nunito', sans-serif;
      margin: 0;
      padding: 0;
      min-height: 100vh;
      background-color: #0c1f3f;
      background-image: url('https://images.unsplash.com/photo-1518050346340-aa2ec3bb424b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8Y2FzdGxlJTIwYXQlMjBuaWdodHxlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=1800&q=80');
      background-size: cover;
      background-position: center;
      background-repeat: no-repeat;
      color: #fff;
      text-align: center;
    }
    .container {
      background-color: rgba(0, 0, 0, 0.7);
      padding: 2rem;
      border-radius: 10px;
      max-width: 800px;
      margin: 2rem auto;
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    h1 {
      font-size: 2.5rem;
      margin-bottom: 1rem;
      color: #7db9ff;
    }
    p {
      font-size: 1.2rem;
      line-height: 1.6;
      margin-bottom: 1.5rem;
    }
    .cta-button {
      display: inline-block;
      background-color: #2b5fb4;
      color: white;
      font-weight: 600;
      padding: 0.8rem 1.5rem;
      border-radius: 5px;
      text-decoration: none;
      transition: all 0.3s ease;
      margin-top: 1rem;
    }
    .cta-button:hover {
      background-color: #3873d1;
      transform: translateY(-2px);
      box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }
    .features {
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 1.5rem;
      margin: 2rem 0;
    }
    .feature {
      flex: 1 1 300px;
      background-color: rgba(43, 95, 180, 0.2);
      padding: 1.5rem;
      border-radius: 8px;
      border-left: 4px solid #2b5fb4;
    }
    .feature h3 {
      color: #7db9ff;
      margin-top: 0;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Children's Castle</h1>
    <p>An engaging, mobile-friendly interactive storytime web application designed for young children, combining educational storytelling with comprehensive game-based learning experiences.</p>
    
    <div class="features">
      <div class="feature">
        <h3>Interactive Stories</h3>
        <p>Explore exciting stories with interactive elements and audio narration to engage young readers.</p>
      </div>
      <div class="feature">
        <h3>Educational Games</h3>
        <p>Play fun, age-appropriate learning games that develop literacy and cognitive skills.</p>
      </div>
      <div class="feature">
        <h3>Progress Tracking</h3>
        <p>Parents can monitor learning achievements with comprehensive progress tracking.</p>
      </div>
    </div>
    
    <a href="https://childrencastle.replit.app" class="cta-button">Enter the Full Application</a>
    
    <p style="margin-top: 2rem; font-size: 0.9rem;">
      © 2025 Children's Castle. All rights reserved.
    </p>
  </div>

  <script src="/js/shooting-star.js"></script>
  <script>
    document.addEventListener('DOMContentLoaded', function() {
      // Initialize shooting stars effect
      if (typeof initShootingStars === 'function') {
        initShootingStars();
      }
    });
  </script>
</body>
</html>
EOF

echo "===== Preparation complete! ====="
echo "The static assets are now prepared for Firebase Hosting."
echo "Run 'firebase deploy --only hosting' to publish the site."
echo "Your site will be available at https://story-time-fun.web.app"