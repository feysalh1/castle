# Custom Domain Setup Guide for ChildrenCastles.com

This guide explains how to connect your custom domain (childrencastles.com) to the Firebase hosted Children's Castle application.

## Prerequisites

Before you begin, ensure you have:

1. Ownership of the domain: childrencastles.com
2. Access to the domain's DNS settings (typically through your domain registrar)
3. Administrator access to the Firebase project

## Step 1: Configure Firebase Hosting for Custom Domain

1. Sign in to the [Firebase Console](https://console.firebase.google.com/)
2. Select your project: **story-time-fun**
3. In the left navigation menu, go to **Hosting**
4. Click **Add custom domain**
5. Enter your domain: **childrencastles.com**
6. Choose whether to also add **www.childrencastles.com** as a subdomain
7. Click **Continue**

## Step 2: Verify Domain Ownership

Firebase will guide you through Google's domain verification process:

1. Choose one of the verification methods:
   - Add a TXT record to your DNS settings
   - Upload an HTML file to your current web hosting
   - Add a CNAME record to your DNS settings
   
2. For the TXT record method (recommended):
   - Go to your domain registrar's DNS management page
   - Add a TXT record with the provided host name and value
   - Return to Firebase and click **Verify**
   
3. Wait for verification to complete (may take up to 24 hours)

## Step 3: Configure DNS Settings

After verification, Firebase will provide DNS records to add:

1. A records for the root domain (childrencastles.com)
2. CNAME record for the www subdomain (if selected)

Example settings:

**A Records** (for childrencastles.com):
```
A @ 151.101.1.195
A @ 151.101.65.195
```

**CNAME Record** (for www.childrencastles.com):
```
CNAME www childrencastles.com
```

## Step 4: Add SSL Certificate

Firebase automatically provisions SSL certificates through Let's Encrypt:

1. In the Firebase Hosting page, your domain will show "Awaiting certificate provisioning"
2. This typically happens within 24 hours after DNS propagation
3. No action required on your part

## Step 5: Additional Subdomains for Cloud Run Backend (Optional)

If you want to also map app.childrencastles.com to your Cloud Run backend:

1. In Google Cloud Console, go to **Cloud Run** > **your-service**
2. Click **Domain Mappings** > **Add Mapping**
3. Enter **app.childrencastles.com**
4. Follow verification steps similar to the Firebase process
5. Add the provided DNS records to your domain registrar

## Troubleshooting

### Domain Verification Issues

- **TXT Record Not Detected**: DNS changes can take 24-48 hours to propagate
- **Verification Timeout**: Try an alternative verification method
- **DNS Settings Errors**: Double-check record types and values

### SSL Certificate Issues

- **Certificate Provisioning Failed**: Verify DNS settings are correct
- **Certificate Expired**: Firebase automatically renews certificates
- **Mixed Content Warnings**: Ensure all resources use HTTPS

### Domain Not Resolving

- **Browser Cache**: Clear your browser cache or try a different browser
- **DNS Propagation**: Wait 24-48 hours for DNS changes to propagate
- **Incorrect A Records**: Verify the IP addresses match Firebase's provided values

## Testing Your Custom Domain

Once setup is complete:

1. Visit https://childrencastles.com in your browser
2. The site should load with a valid SSL certificate (secure padlock icon)
3. Test all functionality to ensure routing is working properly

## Step 6: Configure Firebase Storage for Custom Domain (New Feature)

The Photos feature in Children's Castle now uses Firebase Storage for improved scalability and content delivery. Follow these steps to configure it with your custom domain:

1. **Update CORS Settings**:
   
   Create a file named `cors-config.json`:
   ```json
   [
     {
       "origin": ["https://childrencastles.com", "https://www.childrencastles.com", "https://app.childrencastles.com"],
       "method": ["GET", "HEAD"],
       "maxAgeSeconds": 3600
     }
   ]
   ```

2. **Apply CORS Configuration**:
   ```bash
   gsutil cors set cors-config.json gs://story-time-fun.appspot.com
   ```

3. **Update Cloud Run Environment Variables**:
   ```bash
   gcloud run services update children-castle-app \
     --update-env-vars="USE_FIREBASE_STORAGE=true"
   ```

4. **Test Photos Functionality**:
   - Upload photos in the application
   - Verify thumbnails and full-size images load correctly
   - Check that the URLs use Firebase Storage paths

## Resources

- [Firebase Custom Domain Documentation](https://firebase.google.com/docs/hosting/custom-domain)
- [Firebase Storage Documentation](https://firebase.google.com/docs/storage)
- [Let's Encrypt SSL Certificates](https://letsencrypt.org/)
- [DNS Propagation Checker](https://www.whatsmydns.net/)