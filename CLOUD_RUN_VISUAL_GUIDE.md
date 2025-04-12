# Visual Guide to Deploying Children's Castle on Cloud Run

This step-by-step guide includes screenshots and detailed instructions for deploying the application with Google Cloud Run and Firebase.

## Step 1: Setup Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select an existing one:

   ![Create New Project](https://storage.googleapis.com/gweb-cloudblog-publish/images/new_project.max-700x700.png)

3. Note your Project ID - you'll need it for deployment

## Step 2: Enable Required APIs

1. Go to "APIs & Services" > "Library"
2. Search for and enable the following APIs:
   - Cloud Run API
   - Cloud Build API
   - Container Registry API
   - Firebase Hosting API

   ![Enable APIs](https://storage.googleapis.com/gweb-cloudblog-publish/images/enable_apis.max-700x700.png)

## Step 3: Setup Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com)
2. Add a project, selecting the same Google Cloud project:

   ![Add Firebase Project](https://miro.medium.com/max/1400/1*M-OlzBHUXSyLqGGUK4j9lA.png)

3. Navigate to "Authentication" and enable Google sign-in method
4. Add your application domain to the authorized domains list

## Step 4: Configure Secrets and Environment Variables

1. Collect all necessary API keys and credentials:
   - DATABASE_URL
   - OPENAI_API_KEY
   - FIREBASE_API_KEY
   - FIREBASE_PROJECT_ID
   - FIREBASE_APP_ID
   - ELEVENLABS_API_KEY

2. Either update the `cloudbuild.yaml` file directly or use the `deploy_to_cloud_run.sh` script that prompts for these values

## Step 5: Deploy Using the Terminal

1. Open a terminal in your project directory
2. Make the deployment script executable:
   ```
   chmod +x deploy_to_cloud_run.sh
   ```

3. Run the deployment script:
   ```
   ./deploy_to_cloud_run.sh
   ```

4. Follow the prompts to provide API keys and configuration

## Step 6: Alternative Manual Deployment

If you prefer to deploy manually:

1. Build and push the Docker container:
   ```
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/childrens-castle
   ```

2. Deploy to Cloud Run:
   ```
   gcloud run deploy childrens-castle \
     --image gcr.io/YOUR_PROJECT_ID/childrens-castle \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars="DATABASE_URL=YOUR_DATABASE_URL,OPENAI_API_KEY=YOUR_OPENAI_KEY,..."
   ```

3. Deploy to Firebase Hosting:
   ```
   firebase deploy --only hosting
   ```

## Step 7: Verify Deployment

1. After deployment, check your Firebase Hosting URL:
   ```
   https://YOUR_PROJECT_ID.web.app
   ```

2. Test all functionality:
   - Login with different methods
   - Access story and game modes
   - Verify database connections
   - Test audio generation

## Step 8: Custom Domain Setup

1. In Firebase Console, go to Hosting > Add custom domain
2. Enter your domain (e.g., childrencastles.com)
3. Verify domain ownership by adding TXT record
4. Add the A records and CNAME records as instructed:

   ![Custom Domain Setup](https://firebase.google.com/docs/hosting/images/custom-domain-dns-settings.png)

5. Wait for DNS propagation and SSL certificate issuance

## Troubleshooting

If you encounter issues:

1. Check Cloud Run logs:
   ```
   gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=childrens-castle"
   ```

2. Verify environment variables are set correctly:
   ```
   gcloud run services describe childrens-castle
   ```

3. Check Firebase Hosting configuration:
   ```
   firebase hosting:sites:get
   ```

4. Ensure your Firebase configuration in the app points to the correct project