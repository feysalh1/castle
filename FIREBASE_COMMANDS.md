# Firebase CLI Commands Reference

This document provides a reference for common Firebase CLI commands you might need for your Children's Castle project.

## Authentication Commands

```bash
# Log in to Firebase
firebase login

# Log in and get a CI token (for non-interactive environments)
firebase login:ci

# Log out from Firebase
firebase logout
```

## Project Commands

```bash
# List your Firebase projects
firebase projects:list

# Set active project
firebase use <project-id>

# Add a project alias
firebase use --add

# Switch between project aliases
firebase use <alias>
```

## Deployment Commands

```bash
# Deploy everything
firebase deploy

# Deploy only hosting
firebase deploy --only hosting

# Deploy with a specific target
firebase deploy --only hosting:<target>

# Deploy with token (CI environments)
firebase deploy --token "<YOUR_TOKEN>" --only hosting
```

## Hosting Commands

```bash
# Initialize hosting
firebase init hosting

# Serve locally before deploying
firebase serve --only hosting

# List hosting sites
firebase hosting:sites:list

# Create a new site
firebase hosting:sites:create <site-name>

# Delete a site
firebase hosting:sites:delete <site-name>
```

## Configuration Commands

```bash
# Initialize Firebase features
firebase init

# Get current config
firebase functions:config:get

# Set config values
firebase functions:config:set key=value

# Clone Firebase config to environment file
firebase functions:config:get > .runtimeconfig.json
```

## Testing and Debugging

```bash
# Serve Firebase locally
firebase serve

# View recent deploys
firebase hosting:releases

# View hosting channel details
firebase hosting:channel:list

# View logs
firebase functions:log
```

## Setting up Hosting with Custom Domain

```bash
# Set up custom domain
firebase hosting:sites:update <site-name> --set-default-domain=<domain-name>

# Connect subdomain
firebase hosting:sites:update <site-name> --add-subdomain=<subdomain-name>
```

## CI/CD with GitHub

```bash
# Set up GitHub integration
firebase init hosting:github

# Get GitHub token
firebase hosting:github:connect
```

For your Children's Castle application (Project ID: story-time-fun), the most commonly used commands will be:

```bash
# Deploy to Firebase Hosting
firebase deploy --only hosting

# Or using a token (in CI environments or Replit)
firebase deploy --token "<YOUR_TOKEN>" --only hosting

# Preview locally
firebase serve --only hosting
```

For more information, run `firebase --help` or visit the [Firebase CLI documentation](https://firebase.google.com/docs/cli).