# Setting up GitHub Integration with Firebase for Children's Castle

This guide explains the process of connecting your Children's Castle app to GitHub for continuous deployment via Firebase Hosting.

## Step 1: Create a Firebase Service Account

1. Go to the [Firebase Console](https://console.firebase.google.com/)
2. Select your project: `story-time-fun`
3. Go to Project Settings > Service accounts
4. Click "Generate new private key" button
5. Save the JSON file securely - you'll need this for GitHub secrets

## Step 2: Set Up GitHub Repository

1. Create a new repository on GitHub or use an existing one
2. Push your Children's Castle app code to the repository
3. Make sure your repository has the following Firebase files:
   - `.firebaserc`: Contains your project ID
   - `firebase.json`: Contains hosting configuration
   - `prepare_github_deploy.sh`: Script for preparing files for deployment
   - `.github/workflows/firebase-deploy.yml`: GitHub Actions workflow file

## Step 3: Configure GitHub Secrets

1. In your GitHub repository, go to Settings > Secrets and variables > Actions
2. Add the following secrets:
   - `FIREBASE_SERVICE_ACCOUNT`: Paste the entire JSON content from step 1
   - `FIREBASE_API_KEY`: Your Firebase API key (from Firebase project settings)
   - `FIREBASE_APP_ID`: Your Firebase App ID (from Firebase project settings)

## Step 4: Configure App Root Directory and Live Branch

### App Root Directory
- By default, the firebase.json file specifies `public` as the root directory for hosting
- Our GitHub Actions workflow automatically creates this directory and copies necessary files
- No changes needed to the app root directory configuration

### Live Branch
- In the GitHub Actions workflow file, we've specified that pushes to the `main` branch trigger live deployment
- If your primary branch is named differently (e.g., `master`), update the workflow file accordingly
- Pull requests to the main branch will create temporary preview URLs for testing

## Step 5: Testing the Integration

1. Make a small change to your codebase
2. Push the change to your GitHub repository
3. Go to the Actions tab in your GitHub repository
4. You should see the workflow running automatically
5. Once complete, your changes will be live at:
   - `https://childrencastles.web.app`
   - `https://childrencastles.com` (if custom domain is configured)

## Step 6: Troubleshooting

If your deployment fails, check the following:

1. GitHub Actions logs for detailed error messages
2. Ensure all secrets are correctly set up
3. Verify the Firebase project ID in `.firebaserc` matches your actual project
4. Check that the service account has the necessary permissions

## Firebase GitHub App (Alternative Approach)

Firebase also offers a GitHub App integration:

1. Go to Firebase Console > Hosting
2. Click "Connect to GitHub"
3. Follow the prompts to install the Firebase GitHub app
4. Select your repository
5. Configure branch and build settings

This approach may be simpler but has fewer customization options than GitHub Actions.

## Additional Resources

- [Firebase GitHub Actions Documentation](https://github.com/marketplace/actions/deploy-to-firebase-hosting)
- [Firebase GitHub App Documentation](https://firebase.google.com/docs/hosting/github-integration)
- [Firebase CLI Documentation](https://firebase.google.com/docs/cli)