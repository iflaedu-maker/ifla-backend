# 🔧 Fix: "Not Found" After Google Login

## Problem
After logging in with Google, you get a "Not Found (404)" error.

## Root Cause
The `GOOGLE_OAUTH2_REDIRECT_URI` environment variable in Render is pointing to `localhost` instead of your production URL.

---

## Fix Step 1: Update Environment Variable in Render

1. Go to **Render Dashboard** → Your `ifla-backend` service
2. Click **"Settings"** tab
3. Scroll to **"Environment Variables"**
4. Find `GOOGLE_OAUTH2_REDIRECT_URI` (or add it if missing)
5. Change it to:
   ```
   https://ifla-backend-9svs.onrender.com/api/auth/google/callback/
   ```
   **Important**: 
   - Use `https://` (not `http://`)
   - Use your exact Render domain
   - Include trailing slash `/`
6. **Save**
7. Wait for auto-redeploy (2-3 minutes)

---

## Fix Step 2: Update Google Cloud Console

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to **APIs & Services** → **Credentials**
3. Click on your OAuth 2.0 Client ID
4. Under **"Authorized redirect URIs"**, make sure you have:
   ```
   https://ifla-backend-9svs.onrender.com/api/auth/google/callback/
   ```
5. If it's not there, click **"ADD URI"** and add it
6. **Save**

**Important**: The redirect URI in Google Console must **exactly match** what's in Render environment variables!

---

## Fix Step 3: Verify Both Match

Make sure these are **EXACTLY the same**:

✅ **Render Environment Variable:**
```
GOOGLE_OAUTH2_REDIRECT_URI=https://ifla-backend-9svs.onrender.com/api/auth/google/callback/
```

✅ **Google Cloud Console Redirect URI:**
```
https://ifla-backend-9svs.onrender.com/api/auth/google/callback/
```

---

## Common Mistakes:

❌ **Wrong:**
- `http://ifla-backend-9svs.onrender.com/api/auth/google/callback/` (no https)
- `https://ifla-backend-9svs.onrender.com/api/auth/google/callback` (missing trailing slash)
- `http://localhost:8000/api/auth/google/callback/` (localhost in production)

✅ **Correct:**
- `https://ifla-backend-9svs.onrender.com/api/auth/google/callback/`

---

## Complete Environment Variables for Google OAuth:

Make sure these are set in Render:

```
GOOGLE_OAUTH2_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_OAUTH2_CLIENT_SECRET=your-client-secret
GOOGLE_OAUTH2_REDIRECT_URI=https://ifla-backend-9svs.onrender.com/api/auth/google/callback/
```

---

## After Fixing:

1. Wait for Render to redeploy
2. Try logging in with Google again
3. It should redirect properly after login

---

## If Still Not Working:

### Check 1: URL Pattern
Make sure the callback URL path exists. It should be:
- Route: `/api/auth/google/callback/`
- View: `accounts.views.google_oauth_callback`

### Check 2: Google Console Settings
Verify in Google Console:
- ✅ Redirect URI is added
- ✅ Client ID and Secret are correct
- ✅ OAuth consent screen is configured

### Check 3: Render Logs
Check Render logs for any errors:
1. Go to Render → Your Service → **Logs**
2. Look for errors related to Google OAuth
3. Common errors:
   - `redirect_uri_mismatch` → Redirect URI doesn't match
   - `invalid_client` → Client ID/Secret wrong
   - `access_denied` → User denied permission

---

## Quick Test:

After updating both places, test:
1. Visit: `https://ifla-backend-9svs.onrender.com/auth/`
2. Click "Continue with Google"
3. Complete Google login
4. Should redirect back and log you in (not show "Not Found")

---

**Remember**: After making changes, wait 2-3 minutes for Render to redeploy!

