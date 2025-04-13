# Comprehensive Setup Guide for Children's Castle

This guide provides detailed instructions for setting up, configuring, and deploying the Children's Castle application.

## Table of Contents

1. [Local Development Setup](#local-development-setup)
2. [Firebase Configuration](#firebase-configuration)
3. [Deployment Process](#deployment-process)
4. [Custom Domain Setup](#custom-domain-setup)
5. [GitHub Integration](#github-integration)
6. [Troubleshooting](#troubleshooting)

## Local Development Setup

### Prerequisites

- Python 3.9+
- Node.js 16+
- PostgreSQL database
- Firebase account

### Environment Configuration

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Update the `.env` file with your credentials:
   ```
   # Database configuration
   DATABASE_URL=postgresql://user:password@localhost:5432/database
   
   # OpenAI configuration
   OPENAI_API_KEY=your_openai_api_key
   
   # ElevenLabs configuration (for voice generation)
   ELEVENLABS_API_KEY=your_elevenlabs_api_key
   
   # Session secret for Flask
   FLASK_SECRET_KEY=your_secret_key_here
   
   # Firebase configuration
   FIREBASE_API_KEY=your_firebase_api_key
   FIREBASE_PROJECT_ID=story-time-fun
   FIREBASE_APP_ID=your_firebase_app_id
   FIREBASE_MEASUREMENT_ID=your_firebase_measurement_id
   FIREBASE_MESSAGING_SENDER_ID=your_firebase_sender_id
   FIREBASE_STORAGE_BUCKET=your_firebase_storage_bucket
   FIREBASE_AUTH_DOMAIN=your_firebase_auth_domain
   ```

### Starting the Application Locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the application:
   ```bash
   python main.py
   ```

## Firebase Configuration

### Setting Up Firebase Project

1. Go to the [Firebase Console](https://console.firebase.google.com/)
2. Create a new project named "story-time-fun" (or use your existing project)
3. Set up Firebase Authentication with Email/Password provider
4. Set up Firebase Hosting
5. Set up Firebase Storage (if needed)
6. Copy the Firebase configuration from Project Settings > Your apps

### Configuring Firebase in the Application

1. Add Firebase configuration to your `.env` file (see above)
2. Verify configuration is working by visiting:
   - `/firebase-test-improved.html` on your local server
   - This should show "Firebase initialized successfully"

## Deployment Process

### Preparing for Deployment

1. Make sure you have the Firebase CLI installed:
   ```bash
   npm install -g firebase-tools
   ```

2. Log in to Firebase:
   ```bash
   firebase login
   ```

3. Run the preparation script:
   ```bash
   chmod +x ./prepare_for_deploy.sh
   ./prepare_for_deploy.sh
   ```

### Deploying to Firebase

Execute the deployment script:
```bash
chmod +x ./deploy.sh
./deploy.sh
```

This will:
1. Verify environment variables are set
2. Prepare Firebase configuration files
3. Build necessary assets
4. Deploy to Firebase Hosting

After deployment, your site will be available at:
- `https://story-time-fun.web.app`
- Your custom domain (if configured)

## Custom Domain Setup

To set up your custom domain `childrencastles.com`:

1. Go to Firebase Console > Hosting > Add custom domain
2. Enter your domain name `childrencastles.com`
3. Verify domain ownership by adding the provided TXT record to your DNS configuration
4. Add the provided A records for your domain:
   ```
   @ A 151.101.1.195
   @ A 151.101.65.195
   ```
5. Add CNAME record for www subdomain:
   ```
   www CNAME story-time-fun.web.app
   ```

For detailed instructions, refer to [CUSTOM_DOMAIN_SETUP.md](./CUSTOM_DOMAIN_SETUP.md)

## GitHub Integration

### Setting Up GitHub Actions for Automated Deployment

1. Push your code to a GitHub repository
2. Generate Firebase token:
   ```bash
   firebase login:ci
   ```
3. Add the token as GitHub Secret named `FIREBASE_TOKEN`
4. Add other Firebase environment variables as GitHub Secrets:
   - `FIREBASE_API_KEY`
   - `FIREBASE_AUTH_DOMAIN`
   - `FIREBASE_PROJECT_ID`
   - `FIREBASE_STORAGE_BUCKET`
   - `FIREBASE_MESSAGING_SENDER_ID`
   - `FIREBASE_APP_ID`
   - `FIREBASE_MEASUREMENT_ID`

5. The GitHub Actions workflow is already configured in `.github/workflows/firebase-deploy.yml`

For detailed instructions, refer to [GITHUB_FIREBASE_DEPLOYMENT.md](./GITHUB_FIREBASE_DEPLOYMENT.md)

## Troubleshooting

### Common Deployment Issues

1. **"Cannot GET /" Error**:
   - Make sure `public/index-firebase.html` exists
   - Verify `firebase.json` has correct rewrite rules

2. **Firebase API Key Errors**:
   - Check that the Firebase API key is correctly set in environment variables
   - Verify the API key is valid in Firebase Console

3. **Deployment Failures**:
   - Check GitHub Actions logs for errors
   - Verify all secrets are correctly set
   - Run `firebase deploy --debug` locally for detailed error information

### Testing Firebase Configuration

You can test your Firebase configuration by:

1. Visiting `/firebase-test-improved.html` on your local server
2. Checking browser console for any errors
3. Verifying the "Firebase initialized successfully" message appears

### Getting Help

If you encounter issues not covered here:

1. Consult the [Firebase Documentation](https://firebase.google.com/docs)
2. Check the [GitHub Actions Documentation](https://docs.github.com/en/actions)
3. Review the Firebase CLI output for specific error messages
4. Reach out to support with detailed error information