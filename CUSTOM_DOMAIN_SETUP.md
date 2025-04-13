# Custom Domain Setup Guide for Firebase Hosting

This guide provides detailed instructions for connecting your custom domain `childrencastles.com` to your Firebase Hosting project.

## Prerequisites

- A Firebase project with Hosting enabled
- Ownership of the domain `childrencastles.com`
- Access to your domain's DNS settings (typically through your domain registrar)

## Step 1: Connect Custom Domain in Firebase Console

1. Go to the [Firebase Console](https://console.firebase.google.com/)
2. Select your project
3. In the left sidebar, click on "Hosting"
4. Click on "Connect domain"
5. Enter your domain name: `childrencastles.com`
6. Click "Continue"

## Step 2: Verify Domain Ownership

Firebase will ask you to verify that you own the domain by adding a TXT record to your DNS settings.

1. In your domain registrar's DNS settings, add the TXT record provided by Firebase:
   ```
   Type: TXT
   Name: @ (or leave blank, depending on your registrar)
   Value: [The verification value provided by Firebase]
   TTL: 3600 (or 1 hour)
   ```

2. Wait for verification to complete (this can take up to 24 hours, but often happens within minutes)
3. In the Firebase Console, click "Verify" once you've added the DNS record

## Step 3: Add Required DNS Records

After verification, Firebase will provide the necessary A records and CNAME records to connect your domain.

### For the Apex Domain (childrencastles.com)

Add the following A records:

```
Type: A
Name: @ (or leave blank, depending on your registrar)
Value: 199.36.158.100
TTL: 3600 (or 1 hour)
```

You may need to add multiple A records with different IP addresses, as specified by Firebase.

### For the www Subdomain (www.childrencastles.com)

Add the following CNAME record:

```
Type: CNAME
Name: www
Value: [Your Firebase app name].web.app
TTL: 3600 (or 1 hour)
```

Replace `[Your Firebase app name]` with your actual Firebase app name (e.g., `story-time-fun.web.app`).

## Step 4: Verify DNS Configuration

1. In the Firebase Console, after adding the DNS records, click "Finish setup"
2. Firebase will check if the DNS records are properly configured
3. This verification can take up to 24 hours as DNS propagation occurs

You can check DNS propagation using online tools like [whatsmydns.net](https://www.whatsmydns.net/) or [dnschecker.org](https://dnschecker.org/).

## Step 5: Set Up SSL Certificate

Firebase Hosting automatically provisions and manages SSL certificates for your custom domain.

1. Once your DNS configuration is verified, Firebase will automatically issue an SSL certificate
2. This process can take up to 24 hours

## Step 6: Test Your Custom Domain

After the DNS propagation and SSL certificate provisioning are complete:

1. Visit your custom domain in a web browser: https://childrencastles.com
2. Verify that your website loads correctly
3. Check that the SSL certificate is working (look for the padlock icon in the browser)

## Step 7: Configure Redirects (Optional)

If you want to redirect all traffic from www to non-www (or vice versa), you can set up redirects in your `firebase.json` file:

```json
{
  "hosting": {
    "redirects": [
      {
        "source": "https://www.childrencastles.com/:path*",
        "destination": "https://childrencastles.com/:path",
        "type": 301
      }
    ]
  }
}
```

## Troubleshooting

### DNS Issues

If your domain isn't connecting properly:

1. Verify all DNS records are entered correctly
2. Check that you've waited long enough for DNS propagation (up to 24 hours)
3. Use DNS checking tools to verify your records
4. Ensure there are no conflicting DNS records for the same domain

### SSL Certificate Issues

If you're seeing SSL certificate warnings:

1. Verify the domain is correctly set up in Firebase Hosting
2. Check that all required DNS records are in place
3. Wait longer for the SSL certificate to be provisioned and propagated
4. Ensure your browser is not caching an old certificate

### Website Not Loading

If your website isn't loading on the custom domain:

1. Verify the domain is correctly pointing to Firebase Hosting by checking the DNS records
2. Make sure your Firebase project is correctly deployed
3. Check if the site works on the default Firebase domain (e.g., `story-time-fun.web.app`)
4. Look for any error messages in the Firebase Console or browser console

## Additional Resources

- [Firebase Custom Domain Documentation](https://firebase.google.com/docs/hosting/custom-domain)
- [Managing SSL Certificates in Firebase](https://firebase.google.com/docs/hosting/custom-domain#ssl)
- [Understanding DNS Records](https://support.google.com/domains/answer/3251147)
- [Firebase Hosting Configuration Guide](https://firebase.google.com/docs/hosting/full-config)