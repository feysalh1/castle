# Getting Children's Castle Live

This guide explains how to deploy Children's Castle to make it live on the web using Firebase Hosting. Follow these instructions to complete the deployment process.

## Prerequisites

Before you start, make sure you have the following:

1. A Firebase account (free tier is sufficient)
2. The Firebase CLI installed (the deployment script will install it if needed)
3. The environment variables set up correctly in your `.env` file
4. Your code pushed to your GitHub repository (if using GitHub Actions)

## Option 1: Manual Deployment (Recommended for First Deployment)

For your first deployment or for testing changes, it's best to deploy manually:

1. Open your terminal in the project directory
2. Make sure you have the latest code
3. Run the deployment script:

   ```bash
   ./deploy.sh
   ```

The script will:
- Check if Firebase CLI is installed and install it if needed
- Run the preparation script to prepare your files
- Ensure all required files exist
- Check if you're logged in to Firebase and prompt you to login if needed
- Deploy your application to Firebase Hosting
- Display the URLs where your application is now available

## Option 2: GitHub Actions Deployment (For Continuous Deployment)

For automatic deployments whenever you push changes to your main branch:

1. Make sure you've set up the GitHub repository with the necessary secrets:
   - `FIREBASE_TOKEN` - Generated using `firebase login:ci`
   - `FIREBASE_API_KEY`
   - `FIREBASE_AUTH_DOMAIN`
   - `FIREBASE_PROJECT_ID`
   - `FIREBASE_STORAGE_BUCKET`
   - `FIREBASE_MESSAGING_SENDER_ID`
   - `FIREBASE_APP_ID`
   - `FIREBASE_MEASUREMENT_ID`

2. Push your changes to the main branch:

   ```bash
   git add .
   git commit -m "Your commit message"
   git push origin main
   ```

3. GitHub Actions will automatically deploy your application when changes are pushed to the main branch.

4. You can monitor the deployment in the "Actions" tab of your GitHub repository.

## Verifying Your Deployment

After deployment, your application will be available at:

- `https://[YOUR_FIREBASE_PROJECT_ID].web.app`
- `https://[YOUR_FIREBASE_PROJECT_ID].firebaseapp.com`

For example, if your Firebase project ID is `story-time-fun`, your URLs would be:
- `https://story-time-fun.web.app`
- `https://story-time-fun.firebaseapp.com`

## Setting Up a Custom Domain (Optional)

If you want to use a custom domain like `childrencastles.com`:

1. Make sure you own the domain
2. Follow the instructions in `CUSTOM_DOMAIN_SETUP.md` to connect your domain to Firebase Hosting

## Troubleshooting Common Deployment Issues

### Firebase CLI Not Found

If you see an error about Firebase CLI not being found:

```
firebase: command not found
```

Run:
```bash
npm install -g firebase-tools
```

### Firebase Authentication Issues

If you have issues logging in to Firebase:

1. Run `firebase logout` and then `firebase login` to refresh your authentication
2. Ensure you have the correct permissions for the Firebase project

### Deployment Failures

If deployment fails with errors:

1. Check that your Firebase project ID in `.firebaserc` matches your actual Firebase project ID
2. Verify that all Firebase configuration variables are correctly set
3. Look for specific error messages in the output that may indicate the issue

### "Cannot GET /" Error After Deployment

If you see a "Cannot GET /" error when visiting your site:

1. Verify that `public/index-firebase.html` exists and is correctly set up
2. Check that the `rewrites` section in `firebase.json` is correctly configured
3. Try deploying again with `firebase deploy --only hosting`

## Getting Help

If you encounter issues not covered here:

1. Check the [Firebase Hosting documentation](https://firebase.google.com/docs/hosting)
2. Run `firebase --help` for command-line help
3. Visit the [Firebase support community](https://firebase.google.com/community)