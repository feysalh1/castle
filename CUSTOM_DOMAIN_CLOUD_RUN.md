# Setting Up a Custom Domain for Children's Castle

This guide will help you connect your custom domain (childrencastles.com) to your Cloud Run service and Firebase hosting.

## Prerequisites

1. You own the domain "childrencastles.com"
2. You have access to your domain's DNS settings
3. Your application is already deployed to Cloud Run and Firebase

## Option 1: Using Firebase Hosting with Custom Domain

### Step 1: Add Custom Domain in Firebase Console

1. Go to the [Firebase Console](https://console.firebase.google.com/) and select your project
2. Navigate to Hosting in the left sidebar
3. Click on "Add custom domain"
4. Enter your domain (childrencastles.com)
5. Follow the verification process, which typically involves:
   - Adding a TXT record to your DNS
   - Waiting for verification (can take up to 24 hours)

### Step 2: Configure DNS Records

Once verified, Firebase will provide you with the required DNS settings:

1. Add the IP addresses as A records in your domain's DNS settings
2. Add the given domain as a CNAME record for www.childrencastles.com (if you want to use www)
3. Wait for DNS propagation (can take up to 48 hours)

## Option 2: Using Cloud Run with Custom Domain

If you prefer to connect the domain directly to Cloud Run:

### Step 1: Add Domain Mapping in Cloud Run

```bash
gcloud run domain-mappings create --service childrens-castle \
  --domain childrencastles.com --region us-central1
```

### Step 2: Configure SSL Certificate

```bash
gcloud beta run domain-mappings update --service childrens-castle \
  --domain childrencastles.com --region us-central1 \
  --certificate-mode=automatic
```

### Step 3: Update DNS Records

Cloud Run will provide you with the required DNS records:

1. Add the given IP addresses as A records in your domain's DNS settings
2. Wait for DNS propagation (can take up to 48 hours)

## Verifying the Custom Domain

After DNS propagation is complete:

1. Visit your custom domain in a browser
2. Verify HTTPS is working properly
3. Test all application functionality

## Troubleshooting

If you encounter issues with your custom domain:

1. Check DNS propagation using [DNSChecker](https://dnschecker.org/)
2. Verify SSL certificate status in Firebase or Cloud Run console
3. Ensure all required DNS records are correctly set up

## DNS Settings Reference

For childrencastles.com, you'll typically need:

```
# For Firebase Hosting
childrencastles.com.        IN    A      151.101.1.195
childrencastles.com.        IN    A      151.101.65.195
www.childrencastles.com.    IN    CNAME  story-time-fun.web.app.

# For Cloud Run (example IPs - use the ones provided)
childrencastles.com.        IN    A      34.120.160.1
childrencastles.com.        IN    A      34.120.160.2
```

Replace the IP addresses with the ones provided by Firebase or Cloud Run.

## Additional Resources

- [Firebase Custom Domain Documentation](https://firebase.google.com/docs/hosting/custom-domain)
- [Cloud Run Custom Domain Documentation](https://cloud.google.com/run/docs/mapping-custom-domains)