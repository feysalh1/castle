# Connecting "childrencastles.com" to Firebase Hosting

This guide will walk you through the exact steps needed to connect your custom domain "childrencastles.com" to your Firebase hosted application.

## Prerequisites

- You have ownership of the domain "childrencastles.com"
- You have access to modify DNS settings at your domain registrar
- Your Firebase project "story-time-fun" is already set up with hosting

## Step 1: Prepare Your Firebase Project

Before connecting your custom domain, make sure your Firebase project and hosting are properly set up:

1. Ensure the `.firebaserc` file has the correct project ID:
   ```json
   {
     "projects": {
       "default": "story-time-fun"
     }
   }
   ```

2. Verify that your `firebase.json` file has proper hosting configuration:
   ```json
   {
     "hosting": {
       "public": "public",
       "ignore": [
         "firebase.json",
         "**/.*",
         "**/node_modules/**"
       ],
       "rewrites": [
         {
           "source": "**",
           "destination": "/index.html"
         }
       ]
     }
   }
   ```

3. Deploy your application to Firebase hosting at least once:
   ```bash
   ./deploy.sh
   ```

## Step 2: Add Custom Domain in Firebase Console

1. Go to the [Firebase Console](https://console.firebase.google.com/)
2. Select your project "story-time-fun"
3. In the left sidebar, navigate to **Hosting**
4. Click on **Add custom domain** button
5. Enter your domain name: `childrencastles.com`
6. Click **Continue**
7. Choose "Verify ownership with TXT record"
8. Firebase will provide you with a TXT record that looks like:
   ```
   _firebase=your-verification-code
   ```
9. **Important:** Copy this verification code

## Step 3: Add Verification TXT Record at Your Domain Registrar

1. Log in to your domain registrar's website where childrencastles.com is registered
2. Navigate to DNS settings or domain management
3. Add a new TXT record with these values:
   - **Type**: TXT
   - **Host/Name**: @ (or leave blank, depending on your registrar)
   - **Value**: The verification code from Firebase (including the `_firebase=` part)
   - **TTL**: 3600 (or 1 hour)
4. Save the changes
5. Return to the Firebase Console and click **Verify**
6. Wait for verification to complete (typically a few minutes)

## Step 4: Add DNS Records for Domain Connection

After verification, Firebase will show you the required A and AAAA records to add:

1. Add these records at your domain registrar:

   **For the root domain (childrencastles.com):**
   - **Type**: A
   - **Host/Name**: @ (or leave blank)
   - **Value**: The IP address provided by Firebase (typically 151.101.1.195)
   - **TTL**: 3600 (or 1 hour)

   - **Type**: AAAA
   - **Host/Name**: @ (or leave blank)
   - **Value**: The IPv6 address provided by Firebase
   - **TTL**: 3600 (or 1 hour)

   **For the www subdomain (www.childrencastles.com):**
   - **Type**: CNAME
   - **Host/Name**: www
   - **Value**: story-time-fun.web.app
   - **TTL**: 3600 (or 1 hour)

2. Save all changes at your domain registrar

## Step 5: Wait for DNS Propagation

DNS changes typically take 15 minutes to 48 hours to fully propagate. During this time:

1. Firebase will automatically provision SSL certificates for your domain
2. The status in Firebase Console will update as the process completes

## Step 6: Update Firebase Authentication Settings

After your domain is connected, you need to add it to the allowed authentication domains:

1. In Firebase Console, go to **Authentication** > **Settings**
2. Scroll to the **Authorized domains** section
3. Click **Add domain**
4. Add both:
   - childrencastles.com
   - www.childrencastles.com
5. Click **Add**

## Step 7: Test Your Custom Domain

After DNS propagation (wait at least 15-30 minutes):

1. Visit https://childrencastles.com in your browser
2. Verify that your site loads correctly with HTTPS
3. Check that the Firebase authentication works

## Troubleshooting

If you encounter issues:

1. **Verification Fails**: Double-check the TXT record for typos and ensure it's set at the root domain level (@)
2. **Domain Not Connecting**: Verify A and AAAA records match exactly what Firebase provided
3. **SSL Certificate Issues**: It can take several hours for SSL certificates to be fully provisioned
4. **Authentication Problems**: Ensure both root domain and www subdomain are added to authorized domains in Firebase Authentication settings

For detailed help, refer to the [Firebase Hosting documentation](https://firebase.google.com/docs/hosting/custom-domain).