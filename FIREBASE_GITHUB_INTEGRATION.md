# GitHub Integration with Firebase for Children's Castle

This guide provides comprehensive instructions for setting up continuous deployment from GitHub to Firebase for the Children's Castle app.

## Workflow Overview

We've configured a GitHub Actions workflow that automatically deploys your changes to Firebase Hosting whenever you push to the main branch. Additionally, it creates preview channels for pull requests so you can test changes before merging.

## Prerequisites

1. A GitHub repository with your Children's Castle app code
2. Firebase project (already set up: `story-time-fun`)
3. GitHub account with admin access to the repository

## Setup Instructions

### Step 1: Configure GitHub Secrets

These secrets are required for the GitHub Actions workflow to authenticate with Firebase:

1. Go to your GitHub repository → Settings → Secrets and variables → Actions
2. Add the following secrets:
   - `FIREBASE_SERVICE_ACCOUNT`: The Firebase service account JSON (get from Firebase Console)
     - Go to Firebase Console → Project Settings → Service accounts
     - Click "Generate new private key" and download the JSON file
     - Copy the entire contents of the JSON file into this secret

### Step 2: GitHub Actions Workflow Configuration

A GitHub Actions workflow file has been created at `.github/workflows/firebase-deploy.yml` with two main jobs:

1. **build_and_deploy**: Deploys to the live channel when pushing to the main branch
2. **deploy_preview**: Creates a temporary preview URL when creating a pull request

This workflow includes:
- Setting up Node.js
- Running preparation script
- Installing Firebase CLI
- Deploying to Firebase Hosting

### Step 3: GitHub Branch Protection (Recommended)

To ensure all changes are properly reviewed before deployment:

1. Go to your GitHub repository → Settings → Branches
2. Add a branch protection rule for the `main` branch:
   - Require pull request reviews before merging
   - Require status checks to pass before merging
   - Include the GitHub Actions workflow as a required status check

### Step 4: Preview Channels for Pull Requests

The workflow automatically creates unique preview channels for each pull request:

1. When you create a pull request, the workflow creates a temporary deployment
2. GitHub will comment on your PR with a unique preview URL (e.g., `https://story-time-fun--pr123.web.app`)
3. You can share this URL with team members to review changes before merging
4. Preview deployments expire after 7 days by default

### Step 5: Deployment Process

Here's how the deployment flow works:

1. **Development**:
   - Create a new branch for your feature/fix
   - Make your changes and commit them
   - Push your branch to GitHub

2. **Pull Request**:
   - Create a pull request from your branch to `main`
   - GitHub Actions automatically creates a preview deployment
   - Review the preview deployment and make any necessary adjustments

3. **Merge & Deploy**:
   - After approval, merge the pull request
   - GitHub Actions automatically deploys to the live site
   - Your changes go live at `https://story-time-fun.web.app` and eventually at `https://childrencastles.com`

## Workflow File Details

Our `.github/workflows/firebase-deploy.yml` includes:

```yaml
name: Firebase Deploy

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build_and_deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Prepare for deployment
        run: |
          chmod +x ./prepare_github_deploy.sh
          ./prepare_github_deploy.sh
      - name: Install Firebase CLI
        run: npm install -g firebase-tools
      - name: Deploy to Firebase
        uses: FirebaseExtended/action-hosting-deploy@v0
        with:
          repoToken: '${{ secrets.GITHUB_TOKEN }}'
          firebaseServiceAccount: '${{ secrets.FIREBASE_SERVICE_ACCOUNT }}'
          projectId: story-time-fun
          channelId: live
          target: hosting
          firebaseHostingSite: story-time-fun

  deploy_preview:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      # Similar steps for preview deployment
```

## Troubleshooting

If you encounter issues with the GitHub Actions deployment:

1. **Authentication Issues**: Check your `FIREBASE_SERVICE_ACCOUNT` secret
   - Ensure it contains the complete JSON with no formatting issues
   - Verify the service account has the necessary deployment permissions

2. **Failed Builds**: Check the GitHub Actions logs
   - Look for specific error messages in the Actions tab of your repository
   - Common issues include missing files or incorrect configuration

3. **Preview URLs Not Working**: Check Firebase hosting settings
   - Ensure preview channels are enabled for your Firebase project
   - Verify the GitHub Action has the correct projectId and site name

4. **Custom Domain Issues**: Domain configuration is separate
   - The GitHub workflow only deploys to the Firebase hosting URL
   - Custom domain configuration is handled through the Firebase Console as described in CUSTOM_DOMAIN_SETUP.md

## Continuous Integration Tips

1. **Automated Testing**: Consider adding testing steps before deployment
2. **Conditional Deployments**: You can add conditions to only deploy certain changes
3. **Environment Variables**: Use GitHub repository environment variables for different environments
4. **Approval Gates**: For critical deployments, add manual approval steps

## Resources

- [Firebase Hosting & GitHub Integration](https://firebase.google.com/docs/hosting/github-integration)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Firebase CLI Reference](https://firebase.google.com/docs/cli)
- [Preview Channels Documentation](https://firebase.google.com/docs/hosting/test-preview-deploy)