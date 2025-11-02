# 🔧 Fix: Bad Request (400) Error

A 400 Bad Request in Django usually means `ALLOWED_HOSTS` is not configured correctly.

## Quick Fix

### Step 1: Check Your Render URL

Your Render app URL looks like: `https://your-app-name.onrender.com`

### Step 2: Update ALLOWED_HOSTS Environment Variable

1. Go to Render Dashboard → Your Web Service
2. Click **"Settings"** tab
3. Scroll to **"Environment Variables"**
4. Find `ALLOWED_HOSTS` (or add it if missing)
5. Set the value to your Render domain:
   ```
   your-app-name.onrender.com
   ```
   **OR** if you want to allow both with/without www:
   ```
   your-app-name.onrender.com,www.your-app-name.onrender.com
   ```

6. Save

### Step 3: Redeploy

Click **"Manual Deploy"** → **"Clear build cache & deploy"**

---

## Common Issues

### Issue 1: ALLOWED_HOSTS Not Set

**Symptom**: 400 Bad Request

**Fix**: Add `ALLOWED_HOSTS` environment variable with your domain

### Issue 2: Wrong Domain in ALLOWED_HOSTS

**Symptom**: Still getting 400

**Fix**: Make sure the domain matches exactly:
- ✅ `your-app-name.onrender.com` (correct)
- ❌ `https://your-app-name.onrender.com` (wrong - no https://)
- ❌ `your-app-name.render.com` (wrong - must be .onrender.com)

### Issue 3: DEBUG Still Set to True

**Check**: Make sure `DEBUG=False` in environment variables

---

## Complete Environment Variables Checklist

Make sure you have these set in Render:

```
ALLOWED_HOSTS=your-app-name.onrender.com
DEBUG=False
SECRET_KEY=your-secret-key-here
ENVIRONMENT=production
DATABASE_URL=(auto-set when database is linked)
```

---

## Still Not Working?

Check Render logs:
1. Go to your service → **"Logs"** tab
2. Look for error messages
3. Common errors:
   - "DisallowedHost at /" → ALLOWED_HOSTS issue
   - "Invalid HTTP_HOST header" → ALLOWED_HOSTS issue
   - Database connection errors → DATABASE_URL issue

