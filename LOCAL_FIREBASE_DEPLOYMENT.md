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

## CI/CD Deployment from Replit (Advanced)

If you want to deploy directly from Replit:

1. Generate a CI token on your local machine:
   ```bash
   firebase login:ci
   ```

2. Copy the token and add it as a secret in Replit:
   - Open your Replit project
   - Go to "Secrets" in the Tools menu
   - Add a new secret with key `FIREBASE_TOKEN` and your token as the value

3. Create a deployment script in Replit:
   ```bash
   #!/bin/bash
   firebase deploy --token "$FIREBASE_TOKEN" --only hosting
   ```

4. Make the script executable and run it when you want to deploy.

## Troubleshooting

If you encounter any issues:

1. Make sure your Firebase billing plan supports hosting
2. Check that your project ID in .firebaserc matches your Firebase project
3. Verify that your public directory contains the correct files
4. Check the Firebase CLI output for specific error messages

For more help, consult the [Firebase Hosting documentation](https://firebase.google.com/docs/hosting).