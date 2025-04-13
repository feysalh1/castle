# Firebase GitHub Integration Guide

This guide explains how to set up continuous deployment from GitHub to Firebase Hosting for your "story-time-fun" project.

## Prerequisites

1. A GitHub account
2. Your Children's Castle code pushed to GitHub repository: https://github.com/feysalh1/castle
3. Firebase project: "story-time-fun-1"
4. Firebase CLI installed locally (for testing)

## Step 1: Create a Firebase Service Account

1. Go to the [Firebase Console](https://console.firebase.google.com/project/story-time-fun-1/settings/serviceaccounts/adminsdk)
2. Select "Project settings" > "Service accounts"
3. Click "Generate new private key"
4. Save the JSON file securely - this contains sensitive credentials!

## Step 2: Add GitHub Secret

1. Go to your GitHub repository: https://github.com/feysalh1/castle
2. Navigate to "Settings" > "Secrets and variables" > "Actions"
3. Click "New repository secret"
4. For the name, enter: `FIREBASE_SERVICE_ACCOUNT`
5. For the value, paste the entire contents of the JSON file from Step 1
6. Click "Add secret"

## Step 3: Enable GitHub Actions

1. In your GitHub repository, click the "Actions" tab
2. You should see a workflow named "Firebase Deploy"
3. Click "I understand my workflows, go ahead and enable them"

## Step 4: Custom Domain Setup

To use your custom domain "childrencastles.com" with Firebase:

1. Go to Firebase Console > Hosting
2. Click "Add custom domain"
3. Enter "childrencastles.com" and follow the verification steps
4. Add the provided TXT record to your domain's DNS settings
5. Once verified, add the A records as instructed by Firebase
6. Wait for DNS propagation (can take up to 48 hours)

## Step 5: Test the Deployment

1. Make a small change to your repository (e.g., update a README)
2. Commit and push the change to the main branch
3. Go to the Actions tab to watch the deployment progress
4. Once complete, your site will be live at:
   - https://story-time-fun-1.web.app
   - https://childrencastles.com (after DNS propagation)

## Preview Channels for Testing

For pull requests, GitHub Actions automatically creates preview channels:

1. Create a new branch for your feature
2. Make changes and create a Pull Request to the main branch
3. GitHub Actions will deploy a preview version
4. A comment will be added to your PR with the preview URL
5. The preview channel expires after 7 days

## Troubleshooting

If deployment fails:

1. Check the GitHub Actions logs for specific error messages
2. Verify the FIREBASE_SERVICE_ACCOUNT secret is correctly set
3. Ensure your firebase.json is properly configured
4. Check if your repository has the necessary files (package.json, public/index.html)
5. Run the prepare_github_deploy.sh script locally to test the setup

## Security Best Practices

1. Never commit Firebase service account keys to your repository
2. Use GitHub secrets for all sensitive information
3. Review permissions for your GitHub repository and Firebase project
4. Regularly rotate your Firebase service account key

## Additional Resources

- [Firebase Hosting Documentation](https://firebase.google.com/docs/hosting)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Firebase GitHub Action](https://github.com/FirebaseExtended/action-hosting-deploy)