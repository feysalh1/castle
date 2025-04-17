# Setting Up Custom Domain "childrencastles.com" with Firebase Hosting

This guide provides step-by-step instructions for connecting the custom domain "childrencastles.com" to your Firebase Hosting project.

## Prerequisites

1. You own the domain "childrencastles.com"
2. You have access to your domain's DNS settings through your domain registrar
3. Your Firebase project is already set up and deployed to Firebase Hosting
4. You have the Firebase CLI installed and are logged in

## Steps to Connect Your Custom Domain

### 1. Add Your Custom Domain in Firebase Console

1. Go to the [Firebase Console](https://console.firebase.google.com/)
2. Select your project "story-time-fun"
3. In the left sidebar, click on "Hosting"
4. Click on "Add custom domain"
5. Enter "childrencastles.com" and click "Continue"
6. Also add "www.childrencastles.com" if you want the www subdomain
7. Verify domain ownership following Firebase's instructions

### 2. Configure DNS Settings at Your Domain Registrar

#### Option A: Using Firebase's Nameservers (Recommended)

Firebase will provide you with nameserver addresses. At your domain registrar:

1. Log in to your domain registrar account
2. Navigate to the DNS settings or nameserver settings
3. Replace the current nameservers with the ones provided by Firebase
4. Save the changes

This may take 24-48 hours to propagate.

#### Option B: Using A Records and CNAME Records

If you prefer not to use Firebase's nameservers, you can add individual DNS records:

1. Log in to your domain registrar account
2. Navigate to the DNS settings
3. Add the A records for the apex domain (childrencastles.com) provided by Firebase
4. Add the CNAME record for the www subdomain (www.childrencastles.com) provided by Firebase
5. Save the changes

### 3. Verify and Wait for SSL Certificate Provisioning

1. After DNS propagation (may take 24-48 hours), Firebase will automatically provision SSL certificates for your domain
2. You can check the status in the Firebase Console under Hosting > Your Domain

### 4. Update Application URLs

Make sure to update references to your application URL in your code:

1. Update any absolute URLs in your application to use the new domain
2. Update Firebase Authentication authorized domains list to include your custom domain
3. Update any external services that might be configured to use your previous domain

## Troubleshooting

1. **DNS Not Propagated**: Use tools like [dnschecker.org](https://dnschecker.org/) to check if your DNS changes have propagated
2. **SSL Certificate Issues**: Ensure your DNS settings exactly match what Firebase provided
3. **Domain Not Working**: Check the Firebase Console for any specific error messages related to your domain

## Maintaining Your Custom Domain

1. Ensure your domain registration is kept up to date
2. If you change DNS providers, you'll need to update your settings again
3. SSL certificates will be automatically renewed by Firebase

## Related Documentation

- [Firebase Custom Domain Documentation](https://firebase.google.com/docs/hosting/custom-domain)
- [Firebase CLI Reference](https://firebase.google.com/docs/cli)