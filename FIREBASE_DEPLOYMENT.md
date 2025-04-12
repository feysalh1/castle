# Firebase Deployment Guide for Children's Castle

This guide explains how to deploy the Children's Castle application to Firebase Hosting with Cloud Run for the backend.

## Prerequisites

1. A Google Cloud account with billing enabled
2. Firebase CLI installed (`npm install -g firebase-tools`)
3. Google Cloud CLI installed (`gcloud` command)

## Step 1: Initialize Firebase Hosting

We've already created the basic configuration files:
- `firebase.json`: Configuration for Firebase Hosting
- `.firebaserc`: Project selection configuration
- `public/index.html`: Landing page for the Firebase site

## Step 2: Deploy to Cloud Run

The Flask application needs to be deployed to Cloud Run:

```bash
# Build and deploy to Cloud Run
gcloud builds submit --tag gcr.io/PROJECT_ID/childrens-castle
gcloud run deploy childrens-castle --image gcr.io/PROJECT_ID/childrens-castle --platform managed
```

Replace `PROJECT_ID` with your Google Cloud project ID.

## Step 3: Configure Firebase Hosting to Connect to Cloud Run

Update the firebase.json file to point to your Cloud Run service:

```json
{
  "hosting": {
    "public": "public",
    "rewrites": [
      {
        "source": "**",
        "run": {
          "serviceId": "childrens-castle",
          "region": "us-central1"
        }
      }
    ]
  }
}
```

## Step 4: Deploy to Firebase Hosting

```bash
# Login to Firebase
firebase login

# Deploy to Firebase Hosting
firebase deploy --only hosting
```

## Step 5: Configure Environment Variables

Set up environment variables in Cloud Run:

```bash
gcloud run services update childrens-castle \
  --set-env-vars="DATABASE_URL=REPLACE_WITH_DATABASE_URL" \
  --set-env-vars="OPENAI_API_KEY=REPLACE_WITH_KEY" \
  --set-env-vars="FIREBASE_API_KEY=REPLACE_WITH_KEY" \
  --set-env-vars="FIREBASE_PROJECT_ID=REPLACE_WITH_PROJECT_ID" \
  --set-env-vars="FIREBASE_APP_ID=REPLACE_WITH_APP_ID" \
  --set-env-vars="ELEVENLABS_API_KEY=REPLACE_WITH_KEY"
```

Replace the placeholder values with your actual environment variables.

## Alternative Deployment Method: Replit Deployments

If you prefer to use Replit's built-in deployment service:

1. Use the Deploy button in the Replit interface
2. Select "Static Site" for the initial landing page
3. Connect your backend to a production database
4. Configure your environment variables in the Replit Secrets manager

## Viewing Your Deployed Site

After successful deployment, your site will be available at:
- Firebase: https://PROJECT_ID.web.app
- Replit: https://PROJECT_NAME.replit.app