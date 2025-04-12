#!/bin/bash
# Script to prepare the Children's Castle application for deployment

echo "===== Preparing Children's Castle for deployment ====="

# Step 1: Create Dockerfile for Cloud Run deployment
echo "Creating Dockerfile..."
cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY pyproject.toml .
COPY requirements.txt* .
COPY .env* .

# Install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt || pip3 install gunicorn flask flask-login flask-sqlalchemy flask-wtf python-dotenv openai firebase-admin elevenlabs psycopg2-binary

# Copy application code
COPY . .

# Expose port
EXPOSE 8080

# Set environment variable for production
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Start the application
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
EOF

# Step 2: Create requirements.txt if it doesn't exist
echo "Creating requirements.txt from packages..."
pip freeze > requirements.txt

# Step 3: Create static site files
echo "Ensuring static site files are ready..."
mkdir -p public/css
mkdir -p public/js
mkdir -p public/images

# Step 4: Create landing page CSS file
echo "Creating CSS for landing page..."
cat > public/css/landing.css << 'EOF'
body {
  font-family: 'Nunito', sans-serif;
  margin: 0;
  padding: 0;
  display: flex;
  justify-content: center;
  align-items: center;
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
  margin: 2rem;
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

@media screen and (max-width: 768px) {
  h1 {
    font-size: 2rem;
  }
  .container {
    margin: 1rem;
    padding: 1.5rem;
  }
}
EOF

# Step 5: Update the index.html to use the separate CSS file
echo "Updating landing page to use separate CSS file..."
cat > public/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Children's Castle - Interactive Storytime</title>
  <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700&display=swap" rel="stylesheet">
  <link href="/css/landing.css" rel="stylesheet">
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
    
    <a href="https://childrencastle.replit.app" class="cta-button">Enter the Castle</a>
    
    <p style="margin-top: 2rem; font-size: 0.9rem;">
      © 2025 Children's Castle. All rights reserved.
    </p>
  </div>
</body>
</html>
EOF

echo "===== Preparation complete! ====="
echo "To deploy to Firebase Hosting with Cloud Run backend:"
echo "1. Run 'firebase login' to log in to your Firebase account"
echo "2. Run 'firebase use --add' to select or create a Firebase project"
echo "3. Deploy the Cloud Run backend using Google Cloud Build"
echo "4. Update firebase.json with your Cloud Run service details"
echo "5. Run 'firebase deploy --only hosting' to deploy the hosting"
echo ""
echo "For more details, see the FIREBASE_DEPLOYMENT.md file."