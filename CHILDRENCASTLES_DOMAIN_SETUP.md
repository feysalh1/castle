# ChildrenCastles.com Domain Setup Guide

This guide provides specific instructions for setting up the childrencastles.com domain with Children's Castle application.

## Domain Configuration Overview

The Children's Castle application uses three key components:

1. **Firebase Hosting** for static content at childrencastles.com
2. **Cloud Run** for the backend application at app.childrencastles.com
3. **Firebase Storage** for photo storage and delivery

## Step 1: Domain Registration & DNS Setup

1. **Domain Registration**: 
   - Register childrencastles.com through your preferred registrar
   - Ensure you have access to DNS settings

2. **DNS Provider Setup**:
   - Point your domain to Cloudflare, Google Domains, or your preferred DNS provider
   - Set up the nameservers as instructed by your DNS provider

## Step 2: Firebase Hosting Configuration

1. **Add Domain to Firebase**:
   ```bash
   firebase hosting:channel:deploy production
   firebase hosting:channel:delete preview
   firebase hosting:sites:add childrencastles.com
   ```

2. **Add Domain Records**:
   In your DNS provider's dashboard, add:
   
   ```
   # A Records for root domain
   A @ 151.101.1.195
   A @ 151.101.65.195
   
   # CNAME for www subdomain
   CNAME www childrencastles.com
   ```

3. **Verify Domain Ownership**:
   - Follow the Firebase console prompts for domain verification
   - Add the TXT record provided by Firebase to your DNS settings

## Step 3: Cloud Run Backend Configuration

1. **Map app Subdomain to Cloud Run**:
   ```bash
   gcloud beta run domain-mappings create \
     --service children-castle-app \
     --domain app.childrencastles.com \
     --region us-central1
   ```

2. **Add DNS Records for app Subdomain**:
   Add the A records provided by Google Cloud to your DNS settings:
   
   ```
   # Example records (actual values will be provided by Google Cloud)
   A app 34.120.160.1
   A app 34.120.160.2
   A app 34.120.160.3
   A app 34.120.160.4
   ```

## Step 4: Firebase Storage Configuration

1. **Configure CORS for the Domain**:
   Create a file named `cors-config.json`:
   
   ```json
   [
     {
       "origin": [
         "https://childrencastles.com", 
         "https://www.childrencastles.com", 
         "https://app.childrencastles.com"
       ],
       "method": ["GET", "HEAD"],
       "maxAgeSeconds": 3600
     }
   ]
   ```

2. **Apply CORS Configuration**:
   ```bash
   gsutil cors set cors-config.json gs://story-time-fun.appspot.com
   ```

3. **Enable Firebase Storage in Environment**:
   ```bash
   gcloud run services update children-castle-app \
     --update-env-vars="USE_FIREBASE_STORAGE=true"
   ```

## Step 5: SSL Certificates

1. **Firebase Hosting SSL**:
   - Firebase automatically provisions SSL certificates through Let's Encrypt
   - This typically happens within 24 hours after DNS propagation

2. **Cloud Run SSL**:
   - Google Cloud automatically provisions SSL certificates for mapped domains
   - This typically happens within 24 hours after DNS propagation

## Step 6: Verification and Testing

1. **Test Main Website**:
   - Visit https://childrencastles.com
   - Verify SSL certificate is valid
   - Check that static content loads correctly

2. **Test Backend Application**:
   - Visit https://app.childrencastles.com
   - Verify authentication and dynamic content
   - Test photo uploads and retrieval

3. **Test Firebase Storage**:
   - Upload photos through the application
   - Inspect URLs to confirm Firebase Storage usage
   - Verify thumbnails and full-size photos load correctly

## Contact Information

For domain registration and DNS assistance:
- Technical Contact: [Your Email]
- Domain Registrar: [Registrar Name]
- DNS Provider: [DNS Provider Name]

## Resources

- [Firebase Custom Domain Documentation](https://firebase.google.com/docs/hosting/custom-domain)
- [Cloud Run Domain Mapping](https://cloud.google.com/run/docs/mapping-custom-domains)
- [Firebase Storage Security](https://firebase.google.com/docs/storage/security)
- [GSUtil CORS Configuration](https://cloud.google.com/storage/docs/configuring-cors)