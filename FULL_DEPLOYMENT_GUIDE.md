# Full Deployment Guide for Children's Castle

This comprehensive guide explains how to deploy the complete Children's Castle application using Firebase Hosting for the frontend and Google Cloud Run for the Flask backend, with GitHub Actions for continuous deployment.

## Architecture Overview

The Children's Castle application uses a hybrid cloud architecture:

1. **Static Content**: Firebase Hosting
   - Landing page
   - Images, CSS, JS files
   - Firebase config files

2. **Dynamic Application**: Google Cloud Run
   - Flask backend
   - Database interactions
   - Authentication logic
   - API endpoints

3. **Continuous Deployment**: GitHub Actions
   - Automated testing
   - Containerization
   - Deployment to both services

## Prerequisites

- GitHub repository with your code
- Firebase project: `story-time-fun`
- Google Cloud project (same project or linked)
- Domain name (optional): `childrencastles.com`
- Docker installed for local testing
- Firebase CLI, Google Cloud SDK installed

## Step 1: Prepare Your Application

### Configure Flask Application

1. Ensure your Flask app binds to the correct port:
   ```python
   if __name__ == "__main__":
       port = int(os.environ.get("PORT", 8080))
       app.run(host="0.0.0.0", port=port)
   ```

2. Set up environment variables:
   - Create `.env.example` with variables needed
   - Document how to set these in Cloud Run

### Configure Firebase Files

1. Ensure `firebase.json` has rewrites for Cloud Run:
   ```json
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
   ```

2. Verify `.firebaserc` has the correct project:
   ```json
   {
     "projects": {
       "default": "story-time-fun"
     }
   }
   ```

### Create or Update Dockerfile

```Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT 8080
ENV PYTHONUNBUFFERED 1

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
```

## Step 2: Create GitHub Actions Workflow

Create a comprehensive workflow file at `.github/workflows/deploy.yml`:

```yaml
name: Build and Deploy

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
          pip install pytest
      - name: Run tests
        run: |
          pytest

  build-and-deploy-cloud-run:
    needs: test
    if: github.event_name == 'push' || github.event_name == 'workflow_dispatch'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Cloud SDK
        uses: google-github-actions/setup-gcloud@v1
        with:
          project_id: story-time-fun
          service_account_key: ${{ secrets.GCP_SA_KEY }}
          
      - name: Configure Docker
        run: |
          gcloud auth configure-docker
          
      - name: Build and push Docker image
        run: |
          docker build -t gcr.io/story-time-fun/children-castle-app:${{ github.sha }} .
          docker push gcr.io/story-time-fun/children-castle-app:${{ github.sha }}
          
      - name: Deploy to Cloud Run
        run: |
          gcloud run deploy children-castle-app \
            --image gcr.io/story-time-fun/children-castle-app:${{ github.sha }} \
            --platform managed \
            --region us-central1 \
            --allow-unauthenticated

  deploy-firebase-hosting:
    needs: [test]
    if: github.event_name == 'push' || github.event_name == 'workflow_dispatch'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          
      - name: Install Firebase CLI
        run: npm install -g firebase-tools
        
      - name: Deploy to Firebase
        uses: FirebaseExtended/action-hosting-deploy@v0
        with:
          repoToken: '${{ secrets.GITHUB_TOKEN }}'
          firebaseServiceAccount: '${{ secrets.FIREBASE_SERVICE_ACCOUNT }}'
          projectId: story-time-fun
          channelId: live
          firebaseHostingSite: story-time-fun

  deploy-preview:
    needs: [test]
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          
      - name: Install Firebase CLI
        run: npm install -g firebase-tools
        
      - name: Create preview channel
        uses: FirebaseExtended/action-hosting-deploy@v0
        with:
          repoToken: '${{ secrets.GITHUB_TOKEN }}'
          firebaseServiceAccount: '${{ secrets.FIREBASE_SERVICE_ACCOUNT }}'
          projectId: story-time-fun
          channelId: 'pr-${{ github.event.number }}'
          firebaseHostingSite: story-time-fun
          expires: '7d'
```

## Step 3: Set Up GitHub Secrets

In your GitHub repository, add these secrets:

1. `FIREBASE_SERVICE_ACCOUNT`: Firebase service account JSON
2. `GCP_SA_KEY`: Google Cloud service account key (with Cloud Run deploy permissions)

## Step 4: Deploy Process Flow

### Development to Production Flow

1. **Local Development**:
   - Run Flask app locally
   - Test features in development environment

2. **Create Feature Branch**:
   - Create a branch for your feature
   - Implement changes and commit

3. **Pull Request**:
   - Create PR to main branch
   - GitHub Actions creates preview deployment
   - Review preview URLs and make adjustments

4. **Merge and Deploy**:
   - After approval, merge PR to main
   - GitHub Actions deploys to:
     - Google Cloud Run (backend)
     - Firebase Hosting (frontend)

5. **Post-Deployment Verification**:
   - Test deployed application
   - Monitor for errors

## Step 5: Custom Domain Setup (Optional)

1. **Set Up Domain in Firebase**:
   - Follow instructions in `CUSTOM_DOMAIN_SETUP.md`

2. **Set Up Domain Mapping in Cloud Run**:
   - Map your domain to the Cloud Run service
   - Configure path patterns (`/app/*`)

## Troubleshooting

### Common Issues and Solutions

1. **Deployment Fails**:
   - Check GitHub Actions logs
   - Verify secrets are correctly set
   - Check Docker build process for errors

2. **App Not Accessible**:
   - Verify Cloud Run service is public
   - Check Firebase rewrite rules
   - Inspect network requests for routing issues

3. **Environment Variables Missing**:
   - Check that all required env vars are set in Cloud Run
   - Verify secrets management

## Maintenance and Monitoring

### Regular Maintenance Tasks

1. **Update Dependencies**:
   - Regularly update Python packages
   - Keep Docker base image current

2. **Security Scanning**:
   - Use GitHub Security scanning
   - Implement Container scanning

### Monitoring

1. **Set Up Monitoring**:
   - Cloud Run metrics
   - Firebase Hosting analytics
   - Error logging to Cloud Logging

2. **Set Up Alerts**:
   - Error rate thresholds
   - Performance degradation
   - Cost anomalies

## Resources

- [Firebase Hosting Documentation](https://firebase.google.com/docs/hosting)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Firebase GitHub Integration](https://firebase.google.com/docs/hosting/github-integration)

## Additional Configuration

### Setup CORS for API Access

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": [
    "https://story-time-fun.web.app",
    "https://childrencastles.com"
]}})
```

### Configure PostgreSQL Connection

Ensure your Cloud Run service has the appropriate environment variables for database connection:

1. Set these in the Cloud Run console:
   - `DATABASE_URL`
   - `PGUSER`
   - `PGPASSWORD`
   - `PGDATABASE`
   - `PGHOST`
   - `PGPORT`

2. Or set them in the deployment command:
   ```bash
   gcloud run deploy children-castle-app \
     --image gcr.io/story-time-fun/children-castle-app:latest \
     --set-env-vars="DATABASE_URL=postgresql://..."
   ```