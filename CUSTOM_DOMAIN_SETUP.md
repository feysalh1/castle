# Custom Domain Setup for Children's Castle

This guide will help you set up your custom domain (childrencastles.com) with Firebase Hosting.

## Prerequisites

1. You own the domain "childrencastles.com"
2. You have access to the domain's DNS settings
3. Your Firebase project is set up and configured

## Step 1: Add Custom Domain in Firebase Console

1. Go to the [Firebase Console](https://console.firebase.google.com/)
2. Select your project (story-time-fun)
3. In the left sidebar, click on "Hosting"
4. Click "Add custom domain"
5. Enter your domain: `childrencastles.com`
6. Select "Add domain"

## Step 2: Verify Domain Ownership

Firebase will provide you with a TXT record to add to your domain's DNS settings:

1. Go to your domain registrar's website (like GoDaddy, Namecheap, Google Domains, etc.)
2. Find the DNS management section
3. Add the TXT record provided by Firebase:
   - Type: TXT
   - Name/Host: @ (or sometimes just leave blank)
   - Value/Data: [The verification string provided by Firebase]
   - TTL: 3600 (or 1 hour)
4. Save the changes

## Step 3: Configure DNS Records

After verification, Firebase will provide A records to point your domain to Firebase Hosting:

1. Go back to your domain registrar's DNS settings
2. Add the A records provided by Firebase:
   - Type: A
   - Name/Host: @ (for the root domain)
   - Value/Data: [IP addresses provided by Firebase, typically multiple]
   - TTL: 3600 (or 1 hour)
3. Optionally, add a CNAME record for the www subdomain:
   - Type: CNAME
   - Name/Host: www
   - Value/Data: childrencastles.web.app
   - TTL: 3600 (or 1 hour)
4. Save the changes

## Step 4: Wait for DNS Propagation

DNS changes can take 24-48 hours to fully propagate across the internet. However, they often take effect much sooner (30 minutes to a few hours).

## Step 5: Test Your Custom Domain

After DNS propagation, visit your custom domain in a web browser:
- https://childrencastles.com
- https://www.childrencastles.com (if you set up the www subdomain)

## Step 6: Set Up SSL Certificate

Firebase automatically provisions and manages SSL certificates for your custom domain. This process happens automatically after the DNS settings are properly configured.

## Troubleshooting

If your custom domain is not working properly:

1. **Check DNS Settings**: Verify that all DNS records are correctly configured according to Firebase's instructions.
2. **Check Domain Status in Firebase Console**: Go to the Hosting section in Firebase Console and check the status of your custom domain.
3. **DNS Propagation**: Remember that DNS changes can take time to propagate.
4. **Clear Browser Cache**: Sometimes browsers cache old DNS information, so try clearing your browser cache or using a different browser.
5. **Contact Firebase Support**: If issues persist, consider reaching out to Firebase support.

## Additional Resources

- [Firebase Custom Domain Documentation](https://firebase.google.com/docs/hosting/custom-domain)
- [Google Cloud DNS Documentation](https://cloud.google.com/dns/docs)