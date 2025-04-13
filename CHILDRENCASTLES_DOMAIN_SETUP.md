# Setting Up childrencastles.com with Firebase Hosting

This guide provides step-by-step instructions for connecting the childrencastles.com domain to your Firebase hosted Children's Castle application.

## Prerequisites

- Ownership of the childrencastles.com domain
- Access to the domain's DNS settings (through your domain registrar like GoDaddy, Namecheap, etc.)
- Firebase project with Hosting enabled

## Step 1: Connect Domain in Firebase Console

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your Children's Castle project
3. In the left sidebar, click on "Hosting"
4. Click on "Add custom domain"
5. Enter "childrencastles.com" and click "Continue"

## Step 2: Verify Domain Ownership

Firebase will provide a TXT record for domain verification:

1. Go to your domain registrar's website and log in to your account
2. Find the DNS management or DNS settings section for childrencastles.com
3. Add the TXT record provided by Firebase:
   ```
   Type: TXT
   Host/Name: @ (or blank, depending on your registrar)
   Value: [Firebase verification value]
   TTL: 3600 (or 1 hour)
   ```
4. Save the changes
5. Return to Firebase Console and click "Verify"

## Step 3: Add DNS Records

After verification, Firebase will provide A records for the apex domain and a CNAME record for the www subdomain:

### A Records for childrencastles.com

Add the following A records:
```
Type: A
Host/Name: @ (or blank)
Value: 199.36.158.100
TTL: 3600 (or 1 hour)
```

You may need to add multiple A records if Firebase provides multiple IP addresses.

### CNAME Record for www.childrencastles.com

Add the following CNAME record:
```
Type: CNAME
Host/Name: www
Value: [Your Firebase app].web.app
TTL: 3600 (or 1 hour)
```

Replace `[Your Firebase app]` with your actual Firebase app name (e.g., story-time-fun).

## Step 4: Set Up www Redirect (Recommended)

For better user experience, set up a redirect from www to non-www (or vice versa):

1. In your Firebase project directory, update your `firebase.json` file:

```json
{
  "hosting": {
    "public": "public",
    "ignore": [
      "firebase.json",
      "**/.*",
      "**/node_modules/**"
    ],
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

2. Deploy the changes with:
```bash
firebase deploy --only hosting
```

## Step 5: Wait for DNS Propagation and SSL Certificate

1. DNS changes can take up to 24 hours to propagate globally
2. Firebase will automatically provision an SSL certificate for your domain
3. The SSL certificate process may take a few hours

## Step 6: Verify the Setup

1. Once DNS propagation and SSL certification are complete, visit https://childrencastles.com
2. Verify that your Children's Castle application loads correctly
3. Check that HTTPS is working properly (look for the padlock icon in the browser)
4. Test the www redirect by visiting https://www.childrencastles.com

## Troubleshooting

### Domain Not Connecting

If childrencastles.com doesn't connect to your Firebase app:

1. Verify your DNS records match exactly what Firebase provided
2. Use online tools like [DNS Checker](https://dnschecker.org/) to confirm DNS propagation
3. Make sure there are no conflicting DNS records

### SSL Certificate Issues

If you see SSL certificate warnings:

1. Make sure you've waited long enough for Firebase to provision the certificate (up to 24 hours)
2. Verify that your domain properly resolves to the Firebase hosting IPs
3. Check that both www and non-www versions of the domain are properly configured

### For Additional Help

If you're still having issues connecting the domain:

1. Review the [Firebase Custom Domain Documentation](https://firebase.google.com/docs/hosting/custom-domain)
2. Contact your domain registrar for help with DNS configuration
3. Check Firebase Console for any specific error messages related to your domain setup