# Firebase Hosting with Cloud Run Integration Guide

This guide explains how to connect your Firebase-hosted frontend with the Flask backend running on Google Cloud Run.

## Overview

The Children's Castle application uses a hybrid deployment model:
1. **Firebase Hosting** for static content (landing page, images, etc.)
2. **Google Cloud Run** for the dynamic Flask backend

With this setup, users will access a single domain, but requests will be routed to different services depending on the URL path.

## Architecture

```
User Request → Firebase Hosting → [Static content OR rewrite to Cloud Run]
                                                    ↓
                                          Flask App on Cloud Run
```

## Prerequisites

1. Firebase Project (`story-time-fun`)
2. Google Cloud Project (linked to Firebase)
3. Domain name (optional: `childrencastles.com`)
4. Firebase CLI installed and configured

## Step 1: Deploy Flask Backend to Cloud Run

First, deploy your Flask application to Cloud Run:

1. Build and push a Docker container with your app:
   ```bash
   # Build the Docker image
   docker build -t gcr.io/story-time-fun/children-castle-app .
   
   # Push to Google Container Registry
   docker push gcr.io/story-time-fun/children-castle-app
   ```

2. Deploy to Cloud Run:
   ```bash
   gcloud run deploy children-castle-app \
     --image gcr.io/story-time-fun/children-castle-app \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

3. Note the assigned URL (e.g., `https://children-castle-app-abc123.run.app`)

## Step 2: Configure Firebase Hosting with Rewrites

Update your `firebase.json` file to include rewrites that direct application requests to Cloud Run:

```json
{
  "hosting": {
    "site": "story-time-fun",
    "public": "public",
    "ignore": [
      "firebase.json",
      "**/.*",
      "**/node_modules/**"
    ],
    "rewrites": [
      {
        "source": "/app/**",
        "run": {
          "serviceId": "children-castle-app",
          "region": "us-central1"
        }
      },
      {
        "source": "**",
        "destination": "/index.html"
      }
    ],
    "headers": [
      {
        "source": "**/*.@(jpg|jpeg|gif|png|svg|webp|js|css|eot|otf|ttf|ttc|woff|woff2|font.css)",
        "headers": [
          {
            "key": "Cache-Control",
            "value": "max-age=604800"
          }
        ]
      }
    ]
  }
}
```

This configuration:
- Routes all `/app/**` requests to your Cloud Run service
- Serves all other requests from Firebase Hosting
- Applies appropriate caching headers

## Step 3: Create or Update Landing Page

Ensure your landing page in Firebase Hosting correctly links to your application:

```html
<a href="/app" class="btn">Enter Children's Castle</a>
```

## Step 4: Deploy to Firebase Hosting

Deploy your configuration to Firebase:

```bash
firebase deploy --only hosting
```

## Step 5: Test the Integration

1. Visit your Firebase Hosting URL: `https://story-time-fun.web.app`
2. Click the "Enter Children's Castle" button
3. You should be directed to your Flask application running on Cloud Run

## Step 6: Set Up Custom Domain (Optional)

To use a custom domain:

1. Add your domain in Firebase Console:
   - Go to Hosting → Add custom domain
   - Follow the verification steps for `childrencastles.com`

2. Configure Cloud Run with the same domain:
   - Go to Cloud Run → your service → Domain mappings
   - Add your domain with path `/app/*`

3. Update DNS settings as instructed by Firebase Console

## Troubleshooting

### Problem: Cloud Run integration not working

**Solution**: Verify the following:
- Cloud Run service is deployed and accessible
- Service is public (allow-unauthenticated)
- Firebase rewrite configuration has the correct service ID
- Firebase project and GCP project are correctly linked

### Problem: CORS errors when accessing Cloud Run from Firebase Hosting

**Solution**:
- Ensure your Flask app has CORS headers configured
- Add the following to your Flask application:
  ```python
  from flask_cors import CORS
  
  app = Flask(__name__)
  CORS(app, resources={r"/api/*": {"origins": "*"}})
  ```

### Problem: Authentication issues between services

**Solution**:
- Set up Firebase Authentication that works across both services
- Configure secure session cookies with the same domain

## Best Practices

1. **Security Headers**:
   - Add appropriate security headers in Firebase Hosting
   - Configure CSP to allow resources from Cloud Run

2. **Environment Variables**:
   - Use Cloud Run environment variables for secrets
   - Keep consistent environment variables between development and production

3. **Monitoring**:
   - Set up Cloud Monitoring for both Firebase Hosting and Cloud Run
   - Configure alerts for error spikes or performance issues

## Resources

- [Firebase Hosting & Cloud Run Integration](https://firebase.google.com/docs/hosting/cloud-run)
- [Google Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Custom Domains in Firebase](https://firebase.google.com/docs/hosting/custom-domain)
- [Cloud Run Domain Mappings](https://cloud.google.com/run/docs/mapping-custom-domains)