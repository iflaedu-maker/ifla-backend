# 🚨 IMMEDIATE FIX: Bad Request (400) Error

Your Render URL is: **`https://ifla-backend-9svs.onrender.com`**

## Fix RIGHT NOW:

1. Go to Render Dashboard → Your Web Service (`ifla-backend`)
2. Click **"Settings"** tab
3. Scroll to **"Environment Variables"**
4. Find or Add **`ALLOWED_HOSTS`**
5. Set the value to:
   ```
   ifla-backend-9svs.onrender.com
   ```
   **NO https://, NO trailing slash, just the domain!**

6. Also verify these are set:
   - `DEBUG` = `False`
   - `ENVIRONMENT` = `production`
   - `SECRET_KEY` = (your secret key)

7. **Save**

8. Render will auto-redeploy. Wait 2-3 minutes.

---

## After Redeploy:

Visit: `https://ifla-backend-9svs.onrender.com`

If still 400, check:
- Did you save the environment variable?
- Wait for redeploy to finish
- Check logs for "DisallowedHost" errors

---

## Complete Environment Variables Needed:

```
ALLOWED_HOSTS=ifla-backend-9svs.onrender.com
DEBUG=False
ENVIRONMENT=production
SECRET_KEY=your-secret-key-here
DATABASE_URL=(should be auto-set from linked database)
CORS_ALLOWED_ORIGINS=https://ifla-backend-9svs.onrender.com
CSRF_TRUSTED_ORIGINS=https://ifla-backend-9svs.onrender.com
```

**Make sure ALLOWED_HOSTS matches your exact domain!**

