# Custom Domain Setup for Children's Castle

This guide walks you through connecting your custom domain "childrencastles.com" to your Firebase Hosting project.

## Step 1: Add Your Custom Domain in Firebase Console

1. Go to the [Firebase Console](https://console.firebase.google.com/project/story-time-fun-1/hosting/sites)
2. Select the "Hosting" section
3. Click "Add custom domain"
4. Enter your domain: `childrencastles.com`
5. Click "Continue"

## Step 2: Verify Domain Ownership

1. Firebase will generate a TXT record for domain verification
2. Add this TXT record to your domain's DNS settings at your domain registrar:
   - Type: TXT
   - Name: @ (or leave empty, depending on your registrar)
   - Value: [The verification code provided by Firebase]
   - TTL: 3600 (or 1 hour)
3. Return to Firebase and click "Verify"
4. It may take some time for DNS changes to propagate (up to 48 hours)

## Step 3: Configure DNS Settings

Once your domain is verified, Firebase will provide you with specific A records:

1. Add the A records to your domain's DNS settings:
   - Type: A
   - Name: @ (or leave empty for the root domain)
   - Value: [IP addresses provided by Firebase, typically multiple records]
   - TTL: 3600 (or 1 hour)

2. If you want to use www.childrencastles.com as well:
   - Add a CNAME record:
   - Type: CNAME
   - Name: www
   - Value: childrencastles.com
   - TTL: 3600 (or 1 hour)

## Step 4: Set Up SSL Certificate

Firebase Hosting automatically provisions and renews SSL certificates for your custom domain. Once your DNS is properly configured:

1. Firebase will begin the SSL provisioning process
2. This may take up to 24 hours to complete
3. You'll see the status in the Firebase Hosting console

## Step 5: Test Your Custom Domain

After DNS propagation and SSL certificate provisioning:

1. Visit your custom domain: https://childrencastles.com
2. Make sure the website loads correctly and SSL is working (green lock icon)
3. Test functionality to ensure everything works as expected

## Troubleshooting

If your custom domain isn't working properly:

1. **DNS Propagation**: Wait 24-48 hours for DNS changes to fully propagate
2. **DNS Configuration**: Double-check your DNS records match exactly what Firebase provided
3. **SSL Issues**: If you see SSL warnings, wait 24 hours for SSL provisioning to complete
4. **Firebase Status**: Check if all Firebase records are correctly added in the Hosting console

## Managing Multiple Domains

If you want to add additional domains later:

1. Follow the same process to add and verify each domain
2. You can manage all your domains from the Firebase Hosting console
3. Each domain will need its own verification and DNS records

## Important Notes

- Keep your domain registration active to maintain control of your domain
- Firebase will handle SSL certificate renewal automatically
- If you change DNS providers, you'll need to re-add the DNS records