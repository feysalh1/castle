# Children's Castle: Complete Deployment Instructions

This guide provides step-by-step instructions for deploying the Children's Castle application using Firebase Hosting for static content and Google Cloud Run for the Flask backend.

## Prerequisites

Before you begin, ensure you have:

1. A Firebase project (story-time-fun)
2. Google Cloud credentials (same project as Firebase)
3. Firebase CLI installed: `npm install -g firebase-tools`
4. Google Cloud SDK installed and configured
5. Domain name (optional): childrencastles.com
6. Git repository with your code

## Deployment Overview

Children's Castle uses a hybrid architecture:
- **Firebase Hosting**: Serves static assets and handles routing
- **Google Cloud Run**: Runs the Flask backend for dynamic content
- **Postgres Database**: Managed by Google Cloud SQL or other provider

## Step 1: Prepare Your Environment Variables

Create a `.env` file with all necessary variables:

```
# Firebase Configuration
FIREBASE_API_KEY=your-api-key
FIREBASE_AUTH_DOMAIN=your-project-id.firebaseapp.com
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_STORAGE_BUCKET=your-project-id.appspot.com
FIREBASE_MESSAGING_SENDER_ID=your-messaging-sender-id
FIREBASE_APP_ID=your-app-id
FIREBASE_MEASUREMENT_ID=your-measurement-id

# Database Configuration
DATABASE_URL=postgresql://username:password@host:port/database?sslmode=require
PGUSER=your-db-user
PGPASSWORD=your-db-password
PGDATABASE=your-db-name
PGHOST=your-db-host
PGPORT=your-db-port

# API Keys
OPENAI_API_KEY=your-openai-key
ELEVENLABS_API_KEY=your-elevenlabs-key

# Application Settings
SESSION_SECRET=your-session-secret

# Firebase Storage Settings
USE_FIREBASE_STORAGE=true  # Enable Firebase Storage for photos in production
```

## Step 2: Deploy to Google Cloud Run

1. Build and deploy the Flask backend:

```bash
# Build the Docker container
docker build -t gcr.io/story-time-fun/children-castle-app:latest .

# Push to Google Container Registry
docker push gcr.io/story-time-fun/children-castle-app:latest

# Deploy to Cloud Run
gcloud run deploy children-castle-app \
  --image gcr.io/story-time-fun/children-castle-app:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="FIREBASE_API_KEY=${FIREBASE_API_KEY},FIREBASE_AUTH_DOMAIN=${FIREBASE_AUTH_DOMAIN},FIREBASE_PROJECT_ID=${FIREBASE_PROJECT_ID},FIREBASE_STORAGE_BUCKET=${FIREBASE_STORAGE_BUCKET},FIREBASE_MESSAGING_SENDER_ID=${FIREBASE_MESSAGING_SENDER_ID},FIREBASE_APP_ID=${FIREBASE_APP_ID},FIREBASE_MEASUREMENT_ID=${FIREBASE_MEASUREMENT_ID},DATABASE_URL=${DATABASE_URL},PGUSER=${PGUSER},PGPASSWORD=${PGPASSWORD},PGDATABASE=${PGDATABASE},PGHOST=${PGHOST},PGPORT=${PGPORT},OPENAI_API_KEY=${OPENAI_API_KEY},ELEVENLABS_API_KEY=${ELEVENLABS_API_KEY},SESSION_SECRET=${SESSION_SECRET},USE_FIREBASE_STORAGE=${USE_FIREBASE_STORAGE}"
```

Or use the provided script:

```bash
./deploy_to_cloud_run.sh
```

2. After deployment, note the Cloud Run service URL:
   - Example: `https://children-castle-app-abcdef123-uc.a.run.app`

## Step 3: Configure Firebase Hosting

1. Update `firebase.json` with the Cloud Run service:

```json
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
    ]
  }
}
```

2. Deploy to Firebase Hosting:

```bash
firebase deploy --only hosting
```

Or use the provided script:

```bash
./deploy_firebase.sh
```

## Step 4: Set Up Custom Domain (Optional)

### Firebase Hosting Domain

1. In the Firebase console, go to Hosting > Add custom domain
2. Enter your domain: `childrencastles.com`
3. Follow the verification process
4. Update your DNS records as instructed

### Cloud Run Domain Mapping

1. Map your domain to the Cloud Run service:

```bash
gcloud beta run domain-mappings create \
  --service children-castle-app \
  --domain app.childrencastles.com \
  --region us-central1
```

2. Update your DNS records for the subdomain

## Step 5: Verify Your Deployment

1. Test the Firebase hosted content: `https://story-time-fun.web.app`
2. Test the Cloud Run backend: `/app/*` paths should be served by Cloud Run
3. Check Firebase Authentication is working: Sign-in features
4. Verify database connections: User data should persist

## Troubleshooting

### Firebase Issues

- **Authentication Errors**: Check Firebase Configuration in environment variables
- **Hosting Not Updating**: Verify `firebase.json` configuration
- **Missing Static Assets**: Check the "public" directory contents

### Cloud Run Issues

- **Server Errors**: Check Cloud Run logs in Google Cloud Console
- **Environment Variables Missing**: Verify all env vars were set in deployment
- **Database Connection Issues**: Check connection string and SSL settings

### Domain Issues

- **SSL Errors**: Ensure certificates are properly provisioned
- **Routing Issues**: Check `firebase.json` rewrites configuration

## Automatic Deployment with GitHub Actions

For continuous deployment, set up GitHub Actions:

1. Create `.github/workflows/firebase-deploy.yml`:

```yaml
name: Deploy to Firebase Hosting on merge
on:
  push:
    branches: [ main ]
jobs:
  build_and_deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm ci && npm run build
      - uses: FirebaseExtended/action-hosting-deploy@v0
        with:
          repoToken: '${{ secrets.GITHUB_TOKEN }}'
          firebaseServiceAccount: '${{ secrets.FIREBASE_SERVICE_ACCOUNT }}'
          channelId: live
          projectId: story-time-fun
```

2. Create `.github/workflows/cloud-run-deploy.yml`:

```yaml
name: Deploy to Cloud Run on merge
on:
  push:
    branches: [ main ]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: google-github-actions/setup-gcloud@v1
        with:
          service_account_key: ${{ secrets.GCP_SA_KEY }}
          project_id: story-time-fun
      - run: |
          gcloud builds submit --tag gcr.io/story-time-fun/children-castle-app
          gcloud run deploy children-castle-app \
            --image gcr.io/story-time-fun/children-castle-app \
            --platform managed \
            --region us-central1 \
            --allow-unauthenticated \
            --update-env-vars="FIREBASE_API_KEY=${{ secrets.FIREBASE_API_KEY }},FIREBASE_AUTH_DOMAIN=${{ secrets.FIREBASE_AUTH_DOMAIN }},FIREBASE_PROJECT_ID=${{ secrets.FIREBASE_PROJECT_ID }},FIREBASE_STORAGE_BUCKET=${{ secrets.FIREBASE_STORAGE_BUCKET }},FIREBASE_MESSAGING_SENDER_ID=${{ secrets.FIREBASE_MESSAGING_SENDER_ID }},FIREBASE_APP_ID=${{ secrets.FIREBASE_APP_ID }},FIREBASE_MEASUREMENT_ID=${{ secrets.FIREBASE_MEASUREMENT_ID }},DATABASE_URL=${{ secrets.DATABASE_URL }},OPENAI_API_KEY=${{ secrets.OPENAI_API_KEY }},ELEVENLABS_API_KEY=${{ secrets.ELEVENLABS_API_KEY }},SESSION_SECRET=${{ secrets.SESSION_SECRET }},USE_FIREBASE_STORAGE=true"
```

## Firebase Storage Configuration

For the Photos feature, Children's Castle utilizes Firebase Storage for better scalability and content delivery:

1. **Enable Firebase Storage**: Set `USE_FIREBASE_STORAGE=true` in your environment variables
2. **Storage Security Rules**: Configure rules to restrict access to authorized users

```
// Firebase Storage security rules
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    // Authentication required
    match /{allPaths=**} {
      allow read, write: if request.auth != null;
    }
    
    // Allow public access to thumbnails (optional)
    match /photos/thumbnails/{photoId} {
      allow read: if true;
    }
  }
}
```

3. **CORS Configuration**: Set up proper CORS for direct access from browsers

```bash
# Example CORS configuration for Firebase Storage
gsutil cors set cors-config.json gs://story-time-fun.appspot.com
```

cors-config.json:
```json
[
  {
    "origin": ["https://childrencastles.com", "https://story-time-fun.web.app"],
    "method": ["GET", "HEAD"],
    "maxAgeSeconds": 3600
  }
]
```

## Resources

- [Firebase Hosting Documentation](https://firebase.google.com/docs/hosting)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Firebase & Cloud Run Integration](https://firebase.google.com/docs/hosting/cloud-run)
- [Firebase Storage Documentation](https://firebase.google.com/docs/storage)
- [GitHub Actions for Firebase](https://github.com/marketplace/actions/deploy-to-firebase-hosting)
- [GitHub Actions for Google Cloud](https://github.com/google-github-actions/setup-gcloud)