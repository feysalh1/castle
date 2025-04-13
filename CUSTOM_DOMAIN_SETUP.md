# Setting Up Custom Domain with Firebase Hosting

This document provides step-by-step instructions for connecting your custom domain "childrencastles.com" to your Firebase hosted application.

## Prerequisites

- Access to your domain's DNS settings (through your domain registrar)
- Firebase project already set up with hosting
- Firebase CLI installed and authenticated

## Steps to Connect Your Custom Domain

### 1. Add Your Custom Domain in Firebase Console

1. Go to the [Firebase Console](https://console.firebase.google.com/) and select your project "story-time-fun"
2. In the left sidebar, navigate to **Hosting**
3. Click on the **Add custom domain** button
4. Enter your domain name: `childrencastles.com` 
5. Click **Continue**
6. Select "Verify domain ownership with TXT record" if prompted
7. Firebase will provide you with a TXT record to add to your DNS settings

### 2. Verify Domain Ownership

1. Go to your domain registrar's website (e.g., GoDaddy, Namecheap, Google Domains)
2. Navigate to the DNS settings for your domain "childrencastles.com"
3. Add the TXT record provided by Firebase:
   - Type: TXT
   - Host/Name: @ (or leave blank, depending on your registrar)
   - Value: [The verification code from Firebase]
   - TTL: 3600 (or 1 hour)
4. Save the changes
5. Return to the Firebase Console and click "Verify" 
6. Wait for the verification to complete (this might take a few minutes to a few hours)

### 3. Set Up DNS Records for Domain Connection

After verification, Firebase will provide you with specific DNS records to add:

1. Add an A record for your domain:
   - Type: A
   - Host/Name: @ (or leave blank)
   - Value: [IP address provided by Firebase]
   - TTL: 3600 (or 1 hour)

2. Add a AAAA record for IPv6 support:
   - Type: AAAA
   - Host/Name: @ (or leave blank)
   - Value: [IPv6 address provided by Firebase]
   - TTL: 3600 (or 1 hour)
   
3. If you want to set up "www" subdomain (recommended):
   - Add a CNAME record:
   - Type: CNAME
   - Host/Name: www
   - Value: [Your Firebase app URL, e.g., story-time-fun.web.app]
   - TTL: 3600 (or 1 hour)

### 4. Wait for DNS Propagation

DNS changes can take anywhere from a few minutes to 48 hours to propagate worldwide. During this time, your domain may not consistently direct to your Firebase hosting.

### 5. Configure SSL Certificate

Firebase automatically provisions SSL certificates for your custom domain. This process begins after the DNS records are properly set up and may take a few hours to complete.

### 6. Test Your Custom Domain

Once the setup is complete, test your custom domain by navigating to:
- https://childrencastles.com
- https://www.childrencastles.com (if you set up the www subdomain)

### Troubleshooting

If you encounter issues:

1. **Verification Fails**: Double-check your TXT record for typos and ensure it's set for the correct domain.
2. **Domain Not Connecting**: Verify all DNS records are correctly set up and wait for DNS propagation.
3. **SSL Certificate Issues**: If your site shows as "Not Secure," wait longer for SSL provisioning to complete.
4. **Firebase Console Errors**: Check the error messages in Firebase Console for specific guidance.

### Using Firebase CLI for Custom Domain Management

You can also manage your custom domain through the Firebase CLI:

```bash
# Add a custom domain
firebase hosting:sites:update story-time-fun --add=childrencastles.com

# Delete a custom domain
firebase hosting:sites:update story-time-fun --delete=childrencastles.com
```

### Contact Firebase Support

If problems persist, contact Firebase Support through the [Firebase Console](https://console.firebase.google.com/) by clicking on "Support" in the left sidebar.