# GitHub Repository Setup for Children's Castle

This guide provides step-by-step instructions for pushing your Children's Castle application to GitHub and setting up GitHub Actions for Firebase deployment.

## Step 1: Push Code to GitHub

Since GitHub requires authentication, you'll need to complete these steps on your local machine:

```bash
# Clone the repository from Replit (export project first if needed)
git clone https://replit.com/[your-repl-path] childrens-castle
cd childrens-castle

# Set up GitHub as the remote repository
git remote add origin https://github.com/feysalh1/castle.git

# Push the code to GitHub
git push -u origin main
```

Or, to push directly from Replit:

1. Go to GitHub repository: https://github.com/feysalh1/castle
2. Click the green "Code" button and select "Upload files"
3. Drag and drop your files or use the file picker
4. Commit the changes directly to the main branch

## Step 2: Set Up GitHub Secrets

After your code is pushed, you need to add the required secrets for Firebase deployment:

1. Go to your GitHub repository → Settings → Secrets and variables → Actions
2. Add the following secrets:
   - `FIREBASE_SERVICE_ACCOUNT`: The Firebase service account JSON
   - `FIREBASE_API_KEY`: Your Firebase API key 
   - `FIREBASE_APP_ID`: Your Firebase App ID

To get a Firebase service account:
1. Go to the [Firebase Console](https://console.firebase.google.com/)
2. Select your project: `story-time-fun`
3. Go to Project Settings > Service accounts
4. Click "Generate new private key" button
5. Save the JSON file and paste its contents into the GitHub secret

## Step 3: Enable GitHub Actions

1. Go to the "Actions" tab in your GitHub repository
2. You should see the "Firebase Deploy" workflow
3. Click "Enable workflows"
4. If needed, manually run the workflow by clicking "Run workflow"

## Step 4: Verify Deployment

Once GitHub Actions runs successfully:
1. Your site will be deployed to `https://childrencastles.web.app`
2. If you have a custom domain, it will also be available at `https://childrencastles.com`

## Troubleshooting

If deployment fails:
1. Check the GitHub Actions logs for error details
2. Verify all secrets are configured correctly
3. Make sure the Firebase project ID in `.firebaserc` matches your actual project
4. Confirm your GitHub account has appropriate permissions for the repository

---

## Important Files

These files are already set up in your repository for GitHub Actions:

1. `.github/workflows/firebase-deploy.yml` - The GitHub Actions workflow file
2. `prepare_github_deploy.sh` - Script that prepares files for deployment
3. `.firebaserc` - Contains your Firebase project ID
4. `firebase.json` - Firebase hosting configuration

All authentication-related keys are managed through GitHub Secrets, so your sensitive information remains protected.