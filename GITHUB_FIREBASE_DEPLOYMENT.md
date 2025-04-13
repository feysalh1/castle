# GitHub Integration with Firebase for Children's Castle

This guide provides detailed instructions on how to set up GitHub integration with Firebase for automated deployments of your Children's Castle application.

## Prerequisites

1. A GitHub account and repository for your project
2. A Firebase project (our project: `story-time-fun`)
3. Firebase CLI installed and configured locally
4. GitHub account with permissions to create GitHub Actions

## Step 1: Prepare Your GitHub Repository

If you haven't already, push your code to a GitHub repository:

```bash
# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit"

# Add GitHub remote (replace with your repository URL)
git remote add origin https://github.com/yourusername/childrencastle.git

# Push to GitHub
git push -u origin main
```

## Step 2: Generate a Firebase CI Token

You need a Firebase token for GitHub Actions to deploy on your behalf:

```bash
# Login to Firebase
firebase login

# Generate a CI token
firebase login:ci
```

This command will open a browser for authentication and then display a token. **Copy this token** as you'll need it in the next step.

## Step 3: Add the Firebase Token as a GitHub Secret

1. Go to your GitHub repository
2. Click on "Settings" > "Secrets and variables" > "Actions"
3. Click "New repository secret"
4. Name: `FIREBASE_TOKEN`
5. Value: Paste the token you copied from the previous step
6. Click "Add secret"

## Step 4: Create the GitHub Actions Workflow File

Create a `.github/workflows` directory in your repository and add a `firebase-deploy.yml` file:

```bash
mkdir -p .github/workflows
touch .github/workflows/firebase-deploy.yml
```

## Step 5: Configure the Workflow File

Edit the `.github/workflows/firebase-deploy.yml` file with the following content:

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

## Step 6: Add Firebase Secrets to GitHub

Add all Firebase-related environment variables as GitHub Secrets. For each of these, follow the same process as Step 3:

1. `FIREBASE_API_KEY`
2. `FIREBASE_AUTH_DOMAIN`
3. `FIREBASE_PROJECT_ID`
4. `FIREBASE_STORAGE_BUCKET`
5. `FIREBASE_MESSAGING_SENDER_ID`
6. `FIREBASE_APP_ID`
7. `FIREBASE_MEASUREMENT_ID`

## Step 7: Push the Workflow File to GitHub

```bash
git add .github/workflows/firebase-deploy.yml
git commit -m "Add GitHub Action for Firebase deployment"
git push
```

## Step 8: Trigger a Deployment

Now you can trigger a deployment by:

1. Pushing to the main branch, or
2. Manually triggering the workflow from the "Actions" tab in your GitHub repository

## Additional Configuration

### Custom Domain Setup

If you're using the custom domain `childrencastles.com`, make sure you've:

1. Added the domain in the Firebase Console > Hosting
2. Updated your DNS settings according to Firebase's instructions
3. Verified the domain ownership

See our separate `CUSTOM_DOMAIN_SETUP.md` guide for details.

### Troubleshooting Failed Deployments

If deployments fail, check:

1. GitHub Actions logs for errors
2. Verify all secrets are correctly set
3. Ensure your Firebase project permissions are correct
4. Confirm the Firebase token has not expired (they expire after 1 month)

## Conclusion

With this setup, your Children's Castle application will automatically deploy to Firebase Hosting whenever you push changes to the main branch. This streamlines your development workflow and ensures your changes are quickly available to users.

For more details on Firebase Hosting or GitHub Actions, refer to their official documentation:

- [Firebase Hosting Documentation](https://firebase.google.com/docs/hosting)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)