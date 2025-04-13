# Firebase Setup for Children's Castle

This document provides detailed instructions for setting up the Firebase configuration to correctly work with your deployment.

## Key Issues to Resolve

1. API Key validation issues with Firebase
2. Setting up custom domain "childrencastles.com"
3. Configuring GitHub integration for automated deployments

## Step 1: Generate and Download Service Account Credentials

The most reliable way to authenticate Firebase is using a Service Account key:

1. Go to the [Firebase Console](https://console.firebase.google.com/) and select your project "story-time-fun"
2. In the left sidebar, go to **Project settings** (gear icon)
3. Navigate to the **Service accounts** tab
4. Click on **Generate new private key** button
5. Save the JSON file securely - this is sensitive and should not be shared or committed to version control

## Step 2: Create Firebase Environment Variables

Take the service account JSON file and extract the required information:

1. Create/update your `.env` file with these values from your service account JSON:
   ```
   FIREBASE_API_KEY=[from service account or Firebase settings]
   FIREBASE_AUTH_DOMAIN=story-time-fun.firebaseapp.com
   FIREBASE_PROJECT_ID=story-time-fun
   FIREBASE_STORAGE_BUCKET=story-time-fun.appspot.com
   FIREBASE_MESSAGING_SENDER_ID=[from Firebase settings]
   FIREBASE_APP_ID=[from Firebase settings]
   FIREBASE_MEASUREMENT_ID=[from Firebase settings]
   ```

2. For GitHub Actions deployment, add the entire JSON content as a repository secret called `FIREBASE_SERVICE_ACCOUNT`

## Step 3: Fix Firebase Configuration

1. The Firebase configuration in your application should be updated to use these environment variables consistently.
2. Make sure all templates use the same context processor to get Firebase config values.

## Step 4: Connect Custom Domain

Follow these steps to connect "childrencastles.com" to Firebase:

1. Complete the steps in CUSTOM_DOMAIN_SETUP.md
2. After domain connection, update any hardcoded URLs in your code
3. Don't forget to add your custom domain to Firebase Authentication authorized domains

## Step 5: GitHub Integration

Follow these steps for GitHub integration:

1. Make sure `.github/workflows/firebase-deploy.yml` is correctly set up
2. Add the `FIREBASE_SERVICE_ACCOUNT` secret to your GitHub repository
3. Push changes to trigger the first deployment

## Troubleshooting

If you encounter issues with Firebase authentication:

1. Verify all environment variables match exactly with Firebase Console
2. Check the service account has proper permissions
3. Test with a simple standalone HTML file (like public/firebase-test.html)
4. Review Firebase console logs for specific error messages