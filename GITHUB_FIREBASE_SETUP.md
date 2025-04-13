# Setting up GitHub Integration with Firebase for Children's Castle

This guide explains how to set up continuous deployment from GitHub to Firebase for the Children's Castle app.

## Prerequisites

1. A GitHub repository containing your Children's Castle app
2. Firebase project (already set up: `story-time-fun`)
3. GitHub account with admin access to the repository

## Steps to Connect GitHub to Firebase

### Step 1: Set up GitHub Secrets

In your GitHub repository, add the following secrets:

1. Go to your GitHub repository → Settings → Secrets and variables → Actions
2. Add the following secrets:
   - `FIREBASE_SERVICE_ACCOUNT`: The Firebase service account JSON (get from Firebase Console)
   - `FIREBASE_API_KEY`: Your Firebase API key 
   - `FIREBASE_APP_ID`: Your Firebase App ID

### Step 2: Configure Repository Structure

Ensure your repository has the following structure:
- Root directory: This is the main directory of your application
- Firebase configuration files (already set up):
  - `.firebaserc`: Contains project ID
  - `firebase.json`: Contains hosting configuration

### Step 3: Set Branch for Live Deployment

By default, the GitHub Actions workflow is configured to deploy on pushes to the `main` branch. If your primary branch has a different name (like `master`), update the workflow file accordingly.

### Step 4: Test the Deployment

1. Make a small change to your repository
2. Commit and push the change to your main branch
3. Go to GitHub Actions tab in your repository to monitor the deployment
4. Once complete, your app will be available at:
   - https://story-time-fun.web.app
   - https://childrencastles.com (once custom domain is configured)

## Troubleshooting

If you encounter issues with the GitHub Actions deployment:

1. Check that all secrets are correctly set
2. Ensure the service account has the necessary permissions
3. Look at the GitHub Actions logs for detailed error messages
4. Verify that the Firebase project ID in `.firebaserc` matches your actual project ID

## Configuring Preview Channels

Firebase also supports preview channels for testing changes before deploying to production:

1. Update your GitHub Actions workflow to use preview channels for pull requests
2. This creates temporary URLs for testing without affecting the live site

For further help, refer to the Firebase documentation on GitHub integration:
https://firebase.google.com/docs/hosting/github-integration