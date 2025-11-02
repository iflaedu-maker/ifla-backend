# Google OAuth Login Setup Guide

This guide will help you set up Google OAuth authentication so users can sign up and login using their Google accounts.

## Step 1: Create Google OAuth Credentials

### 1.1 Go to Google Cloud Console
1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Sign in with your Google account
3. Create a new project or select an existing one

### 1.2 Enable Google+ API
1. Go to **APIs & Services** → **Library**
2. Search for **"Google+ API"** or **"People API"**
3. Click on it and click **Enable**

**Note**: For newer projects, you may need to enable **"Google Identity Services API"** instead.

### 1.3 Configure OAuth Consent Screen
1. Go to **APIs & Services** → **OAuth consent screen**
2. Choose **External** (unless you have a Google Workspace account)
3. Click **Create**
4. Fill in the required information:
   - **App name**: IFLA (or your app name)
   - **User support email**: Your email
   - **Developer contact information**: Your email
5. Click **Save and Continue**
6. On **Scopes** page, click **Save and Continue** (no scopes needed for basic setup)
7. On **Test users** (if in testing mode), you can add test emails, then click **Save and Continue**
8. Review and go back to **Dashboard**

### 1.4 Create OAuth 2.0 Credentials
1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **OAuth client ID**
3. Select application type: **Web application**
4. Give it a name: **IFLA OAuth Client**
5. **Authorized JavaScript origins**:
   - For development: `http://localhost:8000`
   - For production: `https://yourdomain.com`
6. **Authorized redirect URIs**:
   - For development: `http://localhost:8000/api/auth/google/callback/`
   - For production: `https://yourdomain.com/api/auth/google/callback/`
7. Click **Create**
8. **IMPORTANT**: Copy both the **Client ID** and **Client Secret** - you'll need these!

---

## Step 2: Configure Your Django Application

### 2.1 Set Environment Variables

Add these to your `.env` file or set them as environment variables:

**Development (.env file):**
```env
GOOGLE_OAUTH2_CLIENT_ID=your-client-id-here.apps.googleusercontent.com
GOOGLE_OAUTH2_CLIENT_SECRET=your-client-secret-here
GOOGLE_OAUTH2_REDIRECT_URI=http://localhost:8000/api/auth/google/callback/
```

**Production (set as environment variables):**
```env
GOOGLE_OAUTH2_CLIENT_ID=your-client-id-here.apps.googleusercontent.com
GOOGLE_OAUTH2_CLIENT_SECRET=your-client-secret-here
GOOGLE_OAUTH2_REDIRECT_URI=https://yourdomain.com/api/auth/google/callback/
```

### 2.2 Update Production Redirect URI

**Important**: Make sure the redirect URI in your `.env` file matches:
- Exactly what you entered in Google Cloud Console
- Your actual domain (with `https://` for production)
- Include the trailing slash: `/api/auth/google/callback/`

---

## Step 3: Install Dependencies

Make sure you have the required packages installed:

```bash
pip install -r requirements.txt
```

The required package is `requests` which should already be in your requirements.txt.

---

## Step 4: Run Migrations

The Google OAuth feature requires a new field in your User model:

```bash
python manage.py migrate accounts
```

---

## Step 5: Test Google OAuth

### Development Testing:
1. Make sure your Django server is running: `python manage.py runserver`
2. Go to your login page: `http://localhost:8000/auth/`
3. Click **"Continue with Google"** button
4. You should be redirected to Google's login page
5. Sign in with a Google account
6. You'll be redirected back and automatically logged in

### Production Testing:
1. Make sure your production server is running
2. Visit your login page
3. Click **"Continue with Google"** button
4. Complete the OAuth flow

---

## How It Works

1. **User clicks "Continue with Google"**
   - Frontend requests Google OAuth URL from backend
   - Backend generates OAuth URL with your credentials
   - User is redirected to Google

2. **User signs in with Google**
   - Google verifies the user
   - Google redirects back to your callback URL with an authorization code

3. **Backend processes the callback**
   - Backend exchanges the code for an access token
   - Backend fetches user info from Google (email, name, etc.)
   - Backend creates a new user OR logs in existing user
   - User is automatically logged in and redirected

---

## Account Linking

The system automatically links Google accounts:

- **New user with Google**: Creates account with Google email and info
- **Existing user (same email)**: Links Google account to existing account
- **Existing user (different email)**: Creates separate account (both can exist)

---

## Troubleshooting

### "Error: redirect_uri_mismatch"
- **Solution**: Make sure the redirect URI in Google Console exactly matches:
  - What's in your `.env` file
  - Your actual domain (including `http://` or `https://`)
  - Includes trailing slash: `/api/auth/google/callback/`

### "Invalid client"
- **Solution**: 
  - Check that `GOOGLE_OAUTH2_CLIENT_ID` and `GOOGLE_OAUTH2_CLIENT_SECRET` are correct
  - Make sure you copied the full Client ID and Secret from Google Console

### "Access blocked: This app's request is invalid"
- **Solution**:
  - Make sure OAuth consent screen is properly configured
  - If in testing mode, add your email as a test user
  - Publish your app for production use (if needed)

### "Error: Google OAuth is not configured"
- **Solution**: 
  - Make sure environment variables are set correctly
  - Restart your Django server after setting environment variables

### Redirect goes to wrong page
- **Solution**: Check that `GOOGLE_OAUTH2_REDIRECT_URI` matches exactly what's in Google Console

---

## Security Best Practices

1. **Never commit credentials to Git**
   - Add `.env` to `.gitignore`
   - Use environment variables in production

2. **Restrict OAuth Credentials**
   - In Google Console, restrict the OAuth client to your domain
   - Set up domain restrictions in **Credentials** → **OAuth 2.0 Client IDs** → **Your Client** → **Application restrictions**

3. **Use HTTPS in Production**
   - Google OAuth requires HTTPS for production
   - Make sure your production site uses SSL/TLS

4. **Rotate Secrets Regularly**
   - Regenerate OAuth credentials periodically
   - Update environment variables when rotating

---

## Production Deployment

### PythonAnywhere
1. Go to **Web** tab → Your web app
2. Scroll to **Environment variables**
3. Add:
   - `GOOGLE_OAUTH2_CLIENT_ID`
   - `GOOGLE_OAUTH2_CLIENT_SECRET`
   - `GOOGLE_OAUTH2_REDIRECT_URI` (with your production domain)

### Heroku
```bash
heroku config:set GOOGLE_OAUTH2_CLIENT_ID=your-client-id
heroku config:set GOOGLE_OAUTH2_CLIENT_SECRET=your-client-secret
heroku config:set GOOGLE_OAUTH2_REDIRECT_URI=https://yourapp.herokuapp.com/api/auth/google/callback/
```

### AWS EC2 / Linux Server
Add to `/etc/environment` or your `.env` file:
```bash
GOOGLE_OAUTH2_CLIENT_ID=your-client-id
GOOGLE_OAUTH2_CLIENT_SECRET=your-client-secret
GOOGLE_OAUTH2_REDIRECT_URI=https://yourdomain.com/api/auth/google/callback/
```

### Windows IIS
1. Open **IIS Manager**
2. Select your site
3. Open **Configuration Editor**
4. Navigate to `system.webServer/aspNetCore/environmentVariables`
5. Add each variable

---

## Quick Reference

| Setting | Example Value |
|---------|---------------|
| **Development Redirect URI** | `http://localhost:8000/api/auth/google/callback/` |
| **Production Redirect URI** | `https://yourdomain.com/api/auth/google/callback/` |
| **Client ID Format** | `xxxxx.apps.googleusercontent.com` |
| **Client Secret Format** | `GOCSPX-xxxxxxxxxxxxx` |

---

## Next Steps

1. ✅ Create Google OAuth credentials
2. ✅ Configure OAuth consent screen
3. ✅ Set environment variables
4. ✅ Run migrations
5. ✅ Test the login flow
6. ✅ Deploy to production

Your Google OAuth integration is now complete! Users can sign up and log in using their Google accounts.

