# Cloud Run Deployment Visual Guide

This document provides a visual guide to deploying Children's Castle to Google Cloud Run.

## Prerequisites

1. A Google Cloud account with billing enabled
2. The Google Cloud SDK (gcloud) installed locally
3. Firebase CLI installed locally
4. Your application code ready for deployment

## Deployment Steps

### 1. Set Up Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project "story-time-fun" or create a new one
3. Enable the Cloud Run API if not already enabled

### 2. Prepare Your Application

1. Make sure your app is listening on the port defined by the `PORT` environment variable:
   ```python
   port = int(os.environ.get('PORT', 5000))
   app.run(host='0.0.0.0', port=port)
   ```

2. Ensure your Dockerfile is correctly set up:
   ```dockerfile
   FROM python:3.11-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   ENV PORT=5000

   CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
   ```

### 3. Build and Deploy Using gcloud

Run the deployment script:
```bash
./deploy_to_cloud_run.sh
```

This will:
1. Build your Docker image
2. Upload it to Google Container Registry
3. Deploy it to Cloud Run

### 4. Configure Firebase Hosting to Work with Cloud Run

1. Update your `firebase.json` file with the correct rewrites:
   ```json
   "rewrites": [
     {
       "source": "/api/**",
       "run": {
         "serviceId": "childrens-castle",
         "region": "us-central1"
       }
     },
     {
       "source": "/**",
       "destination": "/index.html"
     }
   ]
   ```

2. Deploy your Firebase configuration:
   ```bash
   ./deploy_firebase.sh
   ```

### 5. Set Up Custom Domain (Optional)

1. In the Cloud Run console, select your service
2. Click on "Domain Mappings"
3. Click "Add Mapping"
4. Enter your domain (e.g., "api.childrencastles.com")
5. Follow the verification steps

### 6. Testing Your Deployment

1. Visit your Cloud Run URL to verify the backend is working
2. Visit your Firebase Hosting URL to verify the frontend is working
3. Test the integration between frontend and backend

## Troubleshooting

1. **Error: Permission Denied** - Make sure you have the necessary IAM permissions
2. **Error: Service Unavailable** - Check your application logs in Cloud Run
3. **Error: Firebase Hosting not connecting to Cloud Run** - Verify your rewrites in firebase.json

## Additional Resources

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Firebase Hosting with Cloud Run](https://firebase.google.com/docs/hosting/cloud-run)
- [Troubleshooting Cloud Run](https://cloud.google.com/run/docs/troubleshooting)