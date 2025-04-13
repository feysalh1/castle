# GitHub and Firebase Integration Guide

This guide provides detailed instructions for setting up automated deployment from GitHub to Firebase for the Children's Castle application.

## Overview

Using GitHub Actions, we can automatically deploy the Children's Castle application to Firebase Hosting whenever changes are pushed to the main branch. This ensures:

1. Consistent deployment process
2. Automatic environment configuration
3. Fast and reliable updates
4. Version tracking

## Prerequisites

- A GitHub account
- A Firebase project
- Owner or Editor permissions on the Firebase project
- Basic knowledge of Git and GitHub

## Step 1: Configure Your Firebase Project

Ensure your Firebase project is properly set up:

1. Go to the [Firebase Console](https://console.firebase.google.com/)
2. Select your project (or create a new one)
3. Set up Firebase Hosting if not already configured:
   ```bash
   firebase init hosting
   ```
4. Verify your Firebase project ID matches the one in your `.firebaserc` file:
   ```json
   {
     "projects": {
       "default": "your-project-id"
     }
   }
   ```

## Step 2: Create a GitHub Repository

1. Create a new repository on GitHub or use an existing one
2. Push your local code to this repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/childrencastles.git
   git push -u origin main
   ```

## Step 3: Generate Firebase Deployment Token

1. Run the following command to generate a CI token:
   ```bash
   firebase login:ci
   ```
2. A browser window will open. Sign in to Firebase and authorize the CLI
3. Copy the token that appears in your terminal (it starts with `1//...`)

## Step 4: Add Secrets to GitHub Repository

1. Go to your GitHub repository
2. Click on "Settings" > "Secrets and variables" > "Actions"
3. Click "New repository secret"
4. Add the following secrets:

   | Secret Name | Description |
   |-------------|-------------|
   | `FIREBASE_TOKEN` | The token generated in Step 3 |
   | `FIREBASE_API_KEY` | Your Firebase API key |
   | `FIREBASE_AUTH_DOMAIN` | Your Firebase auth domain |
   | `FIREBASE_PROJECT_ID` | Your Firebase project ID |
   | `FIREBASE_STORAGE_BUCKET` | Your Firebase storage bucket |
   | `FIREBASE_MESSAGING_SENDER_ID` | Your Firebase messaging sender ID |
   | `FIREBASE_APP_ID` | Your Firebase app ID |
   | `FIREBASE_MEASUREMENT_ID` | Your Firebase measurement ID |

   You can find these values in your Firebase project settings or in your local `.env` file.

## Step 5: Set Up GitHub Actions Workflow

The workflow file `.github/workflows/firebase-deploy.yml` has already been created and contains:

```yaml
name: Deploy to Firebase Hosting

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build_and_deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install Firebase CLI
        run: npm install -g firebase-tools
      
      - name: Set up environment variables
        run: |
          echo "FIREBASE_API_KEY=${{ secrets.FIREBASE_API_KEY }}" >> $GITHUB_ENV
          echo "FIREBASE_AUTH_DOMAIN=${{ secrets.FIREBASE_AUTH_DOMAIN }}" >> $GITHUB_ENV
          echo "FIREBASE_PROJECT_ID=${{ secrets.FIREBASE_PROJECT_ID }}" >> $GITHUB_ENV
          echo "FIREBASE_STORAGE_BUCKET=${{ secrets.FIREBASE_STORAGE_BUCKET }}" >> $GITHUB_ENV
          echo "FIREBASE_MESSAGING_SENDER_ID=${{ secrets.FIREBASE_MESSAGING_SENDER_ID }}" >> $GITHUB_ENV
          echo "FIREBASE_APP_ID=${{ secrets.FIREBASE_APP_ID }}" >> $GITHUB_ENV
          echo "FIREBASE_MEASUREMENT_ID=${{ secrets.FIREBASE_MEASUREMENT_ID }}" >> $GITHUB_ENV
      
      - name: Prepare for deployment
        run: |
          chmod +x ./prepare_for_deploy.sh
          ./prepare_for_deploy.sh
      
      - name: Deploy to Firebase
        uses: FirebaseExtended/action-hosting-deploy@v0
        with:
          repoToken: '${{ secrets.GITHUB_TOKEN }}'
          firebaseServiceAccount: '${{ secrets.FIREBASE_TOKEN }}'
          projectId: '${{ secrets.FIREBASE_PROJECT_ID }}'
          channelId: live
```

## Step 6: Prepare Your Repository Files

Ensure your repository includes the necessary deployment scripts:

1. `prepare_for_deploy.sh` - This script prepares the application for deployment
2. `.firebaserc` - Contains Firebase project configuration
3. `firebase.json` - Contains Firebase hosting configuration
4. `public/` directory - Contains static files to be deployed

## Step 7: Push to GitHub to Trigger Deployment

1. Make your changes locally
2. Commit and push to the main branch:
   ```bash
   git add .
   git commit -m "Update application"
   git push origin main
   ```
3. This will automatically trigger the GitHub Actions workflow

## Step 8: Monitor Deployment

1. Go to your GitHub repository
2. Click on the "Actions" tab
3. You should see your workflow running
4. Click on the running workflow to see detailed logs
5. Once complete, your site will be updated at your Firebase hosting URL

## Step 9: Manual Deployment Trigger

If you need to manually trigger a deployment without pushing code:

1. Go to your GitHub repository
2. Click on the "Actions" tab
3. Select the "Deploy to Firebase Hosting" workflow
4. Click "Run workflow"
5. Select the branch to deploy from and click "Run workflow"

## Troubleshooting

### Deployment Failures

If your deployment fails, check:

1. GitHub Actions logs for specific error messages
2. Verify all secrets are correctly set
3. Confirm your Firebase token is valid
4. Check that your deployment scripts are executable

### Token Expiration

Firebase CI tokens can expire. If deployments stop working:

1. Generate a new token:
   ```bash
   firebase login:ci
   ```
2. Update the `FIREBASE_TOKEN` secret in GitHub

### Testing Locally

To test your deployment process locally:

1. Set the required environment variables:
   ```bash
   export FIREBASE_API_KEY=your_api_key
   export FIREBASE_PROJECT_ID=your_project_id
   # ...set other variables...
   ```
2. Run the preparation script:
   ```bash
   ./prepare_for_deploy.sh
   ```
3. Deploy manually:
   ```bash
   firebase deploy
   ```

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Firebase Hosting Documentation](https://firebase.google.com/docs/hosting)
- [Firebase CLI Reference](https://firebase.google.com/docs/cli)