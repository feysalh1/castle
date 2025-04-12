# Manual Firebase Deployment for Children's Castle

If you're having issues with the automated deployment script, you can use these manual steps to deploy your application to Firebase Hosting.

## Prerequisites

- Firebase CLI installed (already available in this Replit)
- A Firebase project created and configured
- Your Firebase API key and App ID

## Step 1: Prepare the files

First, run the prepare script to capture the HTML and prepare the files:

```bash
bash ./prepare_for_deploy.sh
```

## Step 2: Login to Firebase (Interactive Mode)

If you're working directly on the Replit interface, you can login interactively:

```bash
firebase login
```

Follow the prompts to complete the authentication process.

## Step 3: Check Firebase Project Configuration

Verify that your Firebase project is correctly configured:

```bash
firebase projects:list
```

Make sure your project `story-time-fun` appears in the list.

## Step 4: Deploy to Firebase

Deploy the application to Firebase Hosting:

```bash
firebase deploy --only hosting
```

This will deploy the content of the `public` directory to Firebase Hosting.

## Step 5: Configure Custom Domain

After deployment, go to the Firebase Console to configure your custom domain:

1. Go to https://console.firebase.google.com
2. Select your project "story-time-fun"
3. Navigate to "Hosting" in the left sidebar
4. Click "Add custom domain"
5. Enter "childrencastles.com" and follow the verification steps
6. Add the required DNS records to your domain registrar

## Using Firebase Deploy with a Service Account

For a more secure approach, you can use a service account instead of a token:

1. Create a service account in the Google Cloud Console
2. Download the service account key JSON file
3. Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable:

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
firebase deploy --only hosting
```

This is the recommended approach for CI/CD deployments.

## Troubleshooting

If you're still having issues with deployment:

1. Make sure your Firebase token or credentials are valid
2. Check that your project ID in `.firebaserc` is correct
3. Try running `firebase use --add` to select your project
4. Check the Firebase Hosting documentation for more help: https://firebase.google.com/docs/hosting