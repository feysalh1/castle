# Local Firebase Deployment Guide

This guide explains how to deploy the Children's Castle application to Firebase Hosting from your local computer.

## Step 1: Download the Project from Replit

First, you need to download the project files from Replit:

1. Click on the three dots (...) in the Replit sidebar
2. Select "Download as zip"
3. Extract the zip file to a folder on your computer

## Step 2: Install Firebase CLI

Install the Firebase CLI on your local machine:

```bash
npm install -g firebase-tools
```

## Step 3: Authenticate with Firebase

```bash
firebase login
```

This will open a browser window where you can log in with your Google account.

## Step 4: Initialize Firebase in the Project

Navigate to the extracted project folder in your terminal:

```bash
cd path/to/extracted/project
```

The project already contains Firebase configuration files, but if you need to initialize a new project:

```bash
firebase init
```

During initialization:
- Select "Hosting: Configure files for Firebase Hosting"
- Choose "Use an existing project" and select your Firebase project
- Specify "public" as your public directory
- Select "yes" for configuring as a single-page app
- Select "no" for GitHub workflow

## Step 5: Deploy to Firebase Hosting

Run the deployment command:

```bash
firebase deploy --only hosting
```

## Step 6: View Your Deployed Site

After successful deployment, your site will be available at:
- https://YOUR-PROJECT-ID.web.app
- https://YOUR-PROJECT-ID.firebaseapp.com

## Using a Custom Domain (Optional)

To use a custom domain:

1. Go to the Firebase Console
2. Select your project
3. Go to Hosting in the left sidebar
4. Click "Add custom domain"
5. Follow the instructions to verify and set up your domain

# Firebase Authentication from Replit

Since Replit is a non-interactive environment, standard `firebase login` won't work. Here's how to authenticate:

## Method 1: Using CI Token (Recommended)

1. **Generate a CI token on your local machine**:
   ```bash
   npm install -g firebase-tools  # If not already installed
   firebase login
   firebase login:ci
   ```
   This will display a token in your terminal.

2. **Add the token as a secret in Replit**:
   - Open your Replit project
   - Click on "Tools" in the left sidebar
   - Select "Secrets"
   - Add a new secret with key `FIREBASE_TOKEN` and paste your token as the value

3. **Create a deployment script in Replit**:
   ```bash
   #!/bin/bash
   # Save this as deploy_firebase.sh
   firebase deploy --token "$FIREBASE_TOKEN" --only hosting
   ```

4. **Make the script executable and run it**:
   ```bash
   chmod +x deploy_firebase.sh
   ./deploy_firebase.sh
   ```

## Method 2: Deploy from GitHub (Alternative)

1. **Push your Replit project to GitHub**
2. **Set up GitHub Actions** with Firebase token as a secret
3. **Configure workflow** to deploy on commits to main branch

## Method 3: Google Cloud Authentication (Advanced)

For more advanced setups, you can use Google Cloud service accounts:

1. Create a service account in Google Cloud Console
2. Generate and download a key file
3. Add the key file contents as a secret in Replit
4. Use the key for authentication:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/keyfile.json"
   firebase deploy --only hosting
   ```

## Troubleshooting

If you encounter any issues:

1. Make sure your Firebase billing plan supports hosting
2. Check that your project ID in .firebaserc matches your Firebase project
3. Verify that your public directory contains the correct files
4. Check the Firebase CLI output for specific error messages

For more help, consult the [Firebase Hosting documentation](https://firebase.google.com/docs/hosting).