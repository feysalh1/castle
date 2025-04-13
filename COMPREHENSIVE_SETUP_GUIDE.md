# Comprehensive Setup Guide for Children's Castle

This guide provides detailed instructions for setting up your Firebase project with custom domain and GitHub integration.

## Table of Contents

1. [Firebase Project Configuration](#1-firebase-project-configuration)
2. [Custom Domain Setup](#2-custom-domain-setup)
3. [GitHub Integration](#3-github-integration)
4. [Firebase API Key Issues](#4-firebase-api-key-issues)
5. [Testing Your Setup](#5-testing-your-setup)

## 1. Firebase Project Configuration

### 1.1 Verify Firebase Project

First, ensure your Firebase project "story-time-fun" is properly set up:

1. Go to the [Firebase Console](https://console.firebase.google.com/)
2. Select your project "story-time-fun"
3. Navigate to Project Settings (gear icon) and verify the project details

### 1.2 Generate Service Account Key

For secure server-side authentication with Firebase:

1. In Firebase Console, go to Project Settings > Service accounts
2. Click "Generate new private key"
3. Save the JSON file securely (do not commit this to your repository)
4. Use this file for secure server-side operations and GitHub Actions

### 1.3 Get Firebase Configuration

For client-side configuration:

1. In Firebase Console, go to Project Settings
2. Scroll down to "Your apps" section
3. If no app is registered, click "Add app" and select Web (</> icon)
4. Register the app with a nickname like "Children's Castle Web"
5. Copy the configuration object that looks like:

```javascript
const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "story-time-fun.firebaseapp.com",
  projectId: "story-time-fun",
  storageBucket: "story-time-fun.appspot.com",
  messagingSenderId: "YOUR_SENDER_ID",
  appId: "YOUR_APP_ID",
  measurementId: "YOUR_MEASUREMENT_ID"
};
```

6. Update your `.env` file with these values

## 2. Custom Domain Setup

### 2.1 Add Custom Domain in Firebase

1. In Firebase Console, navigate to Hosting in the left sidebar
2. Click "Add custom domain"
3. Enter your domain: `childrencastles.com`
4. Click "Continue"
5. Choose verification method (TXT record recommended)
6. Copy the provided TXT record for domain verification

### 2.2 Update DNS Settings

At your domain registrar (e.g., GoDaddy, Namecheap):

1. Log in to your domain registrar's dashboard
2. Navigate to DNS settings for childrencastles.com
3. Add the TXT record provided by Firebase:
   - Type: TXT
   - Host/Name: @ (or leave blank, depending on your registrar)
   - Value: [Verification code from Firebase]
   - TTL: 3600 (or 1 hour)

4. Once verified, add the A and AAAA records provided by Firebase:
   - Type: A
   - Host/Name: @ (or leave blank)
   - Value: [IP address provided by Firebase]
   - TTL: 3600 (or 1 hour)

   - Type: AAAA
   - Host/Name: @ (or leave blank)
   - Value: [IPv6 address provided by Firebase]
   - TTL: 3600 (or 1 hour)

5. Add a CNAME record for the www subdomain:
   - Type: CNAME
   - Host/Name: www
   - Value: story-time-fun.web.app
   - TTL: 3600 (or 1 hour)

### 2.3 Update Authentication Settings

1. In Firebase Console, go to Authentication > Settings
2. In the Authorized domains section, add:
   - childrencastles.com
   - www.childrencastles.com

## 3. GitHub Integration

### 3.1 Prepare GitHub Repository

1. Make sure your code is in a GitHub repository
2. Add the following files to your repository (already created):
   - `.github/workflows/firebase-deploy.yml`
   - `prepare_github_deploy.sh`
   - `.firebaserc`
   - `firebase.json`

### 3.2 Add GitHub Secret

1. Go to your GitHub repository > Settings > Secrets and variables > Actions
2. Click "New repository secret"
3. Name: `FIREBASE_SERVICE_ACCOUNT`
4. Value: Paste the entire content of your service account JSON file
5. Click "Add secret"

### 3.3 Set Up Branch Protection (Recommended)

1. Go to your GitHub repository > Settings > Branches
2. Click "Add rule"
3. Branch name pattern: `main`
4. Check "Require pull request reviews before merging"
5. Check "Require status checks to pass before merging"
6. Add the GitHub Actions workflow as a required status check
7. Click "Create"

## 4. Firebase API Key Issues

If you encounter API key issues, try these solutions:

### 4.1 Verify API Key

1. Check if your API key is correctly copied from Firebase Console
2. Ensure there are no extra spaces or characters
3. Verify the API key is for the correct project

### 4.2 Check API Key Restrictions

1. In Google Cloud Console, go to APIs & Services > Credentials
2. Find your API key and check if it has any restrictions
3. Ensure your domains (localhost, replit.dev, story-time-fun.web.app, childrencastles.com) are in the allowed referrers

### 4.3 Use Service Account Authentication

For server-side operations:
1. Use the Firebase Admin SDK with your service account
2. This provides more secure authentication than API keys

## 5. Testing Your Setup

### 5.1 Test Firebase Configuration

1. Access the test page at `/firebase-config-test.html`
2. Check for "Firebase initialized successfully!" message
3. Review browser console for any errors

### 5.2 Test GitHub Integration

1. Make a small change to your code and push to GitHub
2. Create a pull request to verify preview deployment
3. Merge the pull request to verify production deployment

### 5.3 Test Custom Domain

After DNS propagation (which may take 24-48 hours):
1. Visit https://childrencastles.com
2. Verify the site loads correctly
3. Test authentication flows

## Need Help?

If you encounter issues:
1. Check Firebase logs in Firebase Console > Functions > Logs
2. Review GitHub Actions logs for deployment issues
3. Verify all environment variables and secrets are correctly set
4. Test with the included test pages to isolate configuration issues