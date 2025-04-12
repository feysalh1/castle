# Full Deployment Guide for Children's Castle Application

This guide will help you deploy the complete Children's Castle application with a functioning backend to handle login, user data, and all interactive features.

## Problem Identified

We've identified that our current deployment method creates a static site that doesn't support:
- Login functionality
- User data persistence
- Interactive features that require backend processing

## Solution: Deploy with Cloud Run Backend

To fix this issue, we need to deploy the Flask application to Cloud Run and connect it to Firebase Hosting.

## Step 1: Set Up Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select your existing project
3. Enable the following APIs:
   - Cloud Run API
   - Cloud Build API
   - Container Registry API

## Step 2: Build and Deploy the Container

There are two ways to do this:

### Option A: Using Cloud Build (Recommended)

1. Update the cloudbuild.yaml file with your environment variables if needed

2. Run the following commands:
   ```bash
   # Authenticate with Google Cloud
   gcloud auth login

   # Set your project ID
   gcloud config set project YOUR_PROJECT_ID

   # Submit the build
   gcloud builds submit
   ```

### Option B: Manual Build and Deploy

1. Build the Docker container locally:
   ```bash
   docker build -t gcr.io/YOUR_PROJECT_ID/childrens-castle .
   ```

2. Push to Google Container Registry:
   ```bash
   docker push gcr.io/YOUR_PROJECT_ID/childrens-castle
   ```

3. Deploy to Cloud Run:
   ```bash
   gcloud run deploy childrens-castle \
     --image gcr.io/YOUR_PROJECT_ID/childrens-castle \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

## Step 3: Set Up Environment Variables

Set up your environment variables in Cloud Run:

```bash
gcloud run services update childrens-castle \
  --set-env-vars="DATABASE_URL=YOUR_DATABASE_URL" \
  --set-env-vars="OPENAI_API_KEY=YOUR_OPENAI_KEY" \
  --set-env-vars="FIREBASE_API_KEY=YOUR_FIREBASE_KEY" \
  --set-env-vars="FIREBASE_PROJECT_ID=YOUR_PROJECT_ID" \
  --set-env-vars="FIREBASE_APP_ID=YOUR_APP_ID" \
  --set-env-vars="ELEVENLABS_API_KEY=YOUR_ELEVENLABS_KEY"
```

Replace the placeholders with your actual values.

## Step 4: Deploy to Firebase Hosting

1. Update the firebase.json file (already done) to use Cloud Run as a backend
2. Deploy to Firebase Hosting:
   ```bash
   firebase deploy --only hosting
   ```

## Step 5: Set Up Custom Domain (Optional)

1. If using your own domain (childrencastles.com):
   ```bash
   firebase hosting:channel:deploy --expires 30d live
   ```

2. Add your custom domain in the Firebase Console:
   - Go to Hosting → Add custom domain
   - Follow the instructions to verify domain ownership and set up DNS records

## Checking Deployment

After deployment, you can check the status of your services:

```bash
# Check Cloud Run status
gcloud run services describe childrens-castle

# Check Firebase Hosting status
firebase hosting:sites:list
```

## Troubleshooting

If you encounter issues:

1. Check Cloud Run logs:
   ```bash
   gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=childrens-castle"
   ```

2. Verify environment variables:
   ```bash
   gcloud run services describe childrens-castle --format="value(spec.template.spec.containers[0].env)"
   ```

3. Test the Cloud Run service directly using its URL before testing via Firebase Hosting