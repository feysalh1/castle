# Setting Up Your Custom Domain (childrencastles.com) with Firebase Hosting

This guide will walk you through the process of connecting your custom domain "childrencastles.com" to your Firebase Hosting project.

## Prerequisites
1. You must own the domain "childrencastles.com" and have access to its DNS settings through your domain registrar (e.g., GoDaddy, Namecheap, Google Domains).
2. Your Firebase project must be on the Blaze (pay-as-you-go) plan, as custom domains are not available on the Spark (free) plan.

## Step 1: Add Your Custom Domain in Firebase Console

1. Go to the [Firebase Console](https://console.firebase.google.com/).
2. Select your project (story-time-fun).
3. In the left sidebar, click on "Hosting".
4. Click on "Add custom domain".
5. Enter "childrencastles.com" and click "Continue".
6. Choose whether you want to set up the "www" subdomain as well. We recommend doing this.
7. Follow the verification steps provided by Firebase.

## Step 2: Verify Domain Ownership

1. Firebase will provide you with a TXT record that you need to add to your domain's DNS settings.
2. Log in to your domain registrar's website.
3. Navigate to the DNS or Domain Management section.
4. Add the TXT record with the exact values provided by Firebase:
   - Type: TXT
   - Name/Host: @ (or as specified)
   - Value/Content: (the verification code from Firebase)
   - TTL: Use default (or 3600 seconds/1 hour)
5. Save the changes.
6. Return to Firebase and click "Verify" to confirm ownership.

## Step 3: Add A Records for Domain Pointing

Once verified, Firebase will provide you with A records that need to be added to your domain's DNS settings:

1. Go back to your domain registrar's DNS settings.
2. Add the A records provided by Firebase. Typically, there are 4 records for redundancy:
   - Type: A
   - Name/Host: @ (or as specified)
   - Value/Content: (the IP addresses provided by Firebase, typically Google's load balancing IPs)
   - TTL: Use default (or 3600 seconds/1 hour)
3. For www subdomain (if selected earlier):
   - Follow the Firebase instructions for setting up CNAME records

## Step 4: Wait for DNS Propagation

DNS changes can take anywhere from a few minutes to 48 hours to propagate globally. Typically, it takes 1-24 hours.

## Step 5: Verify the Connection

1. Once propagation is complete, visit your domain in a web browser: https://childrencastles.com
2. If everything is set up correctly, you should see your Children's Castle application.

## Step 6: Set Up SSL Certificate

Firebase Hosting automatically provisions an SSL certificate for your custom domain. This process should happen automatically after DNS propagation.

## Troubleshooting

If your domain isn't working after 24 hours:

1. Check your DNS settings again to ensure they match exactly what Firebase provided.
2. Verify that your domain registration hasn't expired.
3. Use a tool like [DNS Checker](https://dnschecker.org/) to see if your DNS changes have propagated globally.
4. Check the Firebase Console for any error messages or warnings about your custom domain.
5. Ensure your Firebase project is on the Blaze plan.

## Additional Resources

- [Firebase Custom Domain Documentation](https://firebase.google.com/docs/hosting/custom-domain)
- [DNS Propagation Checker](https://www.whatsmydns.net/)
- [Google Domains Help](https://support.google.com/domains/)

For further assistance, contact Firebase support or your domain registrar.