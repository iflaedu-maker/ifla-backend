# 🔧 Complete Fix for 400 Bad Request

## IMMEDIATE ACTION REQUIRED

Go to Render Dashboard → Your Service → **Settings** → **Environment Variables**

### Add/Update These Variables:

1. **ALLOWED_HOSTS**
   ```
   ifla-backend-9svs.onrender.com,*
   ```
   (The `*` allows all hosts temporarily to test)

2. **DEBUG**
   ```
   False
   ```

3. **SECRET_KEY**
   ```
   (your secret key)
   ```

4. **ENVIRONMENT**
   ```
   production
   ```

### Alternative Quick Test:

If you want to test immediately, temporarily set:

```
DEBUG=True
```

This will bypass ALLOWED_HOSTS checking. **BUT** remember to set it back to `False` after testing!

---

## Step-by-Step Fix:

### Option 1: Allow All Hosts (Quick Test)

1. In Render → Settings → Environment Variables
2. Add/Update:
   - `ALLOWED_HOSTS` = `*`
3. Save and wait for redeploy
4. Test your site

**⚠️ Security Note**: `*` allows all hosts. This is for testing only. Once working, change to your specific domain.

### Option 2: Set Exact Domain (Proper Fix)

1. Your exact URL is: `https://ifla-backend-9svs.onrender.com`
2. In Render → Settings → Environment Variables
3. Add/Update:
   - `ALLOWED_HOSTS` = `ifla-backend-9svs.onrender.com`
   - Make sure NO `https://` and NO trailing `/`
4. Save and wait for redeploy

### Option 3: Enable DEBUG Temporarily

1. In Render → Settings → Environment Variables
2. Set:
   - `DEBUG` = `True`
3. Save and redeploy
4. This will show you the actual error message
5. Check the error and fix accordingly

---

## Verify Environment Variables Are Set:

1. Go to Render → Your Service → **Settings**
2. Scroll to **Environment Variables**
3. Make sure you see:
   - ✅ ALLOWED_HOSTS
   - ✅ DEBUG
   - ✅ SECRET_KEY
   - ✅ ENVIRONMENT
   - ✅ DATABASE_URL (should be auto-set)

---

## Check Render Logs for Actual Error:

1. Go to Render → Your Service → **Logs**
2. Look for lines with "400" or "Bad Request"
3. Look for "DisallowedHost" errors
4. Copy the error message - it will tell you exactly what's wrong

---

## Common Issues:

### Issue 1: Variable Not Saving
- Make sure you click **Save** after adding/editing
- Wait a few seconds for it to register

### Issue 2: Redeploy Not Happening
- After saving, Render should auto-redeploy
- If not, go to **Manual Deploy** → **Clear build cache & deploy**

### Issue 3: Still 400 After Fix
- Check logs for the actual error message
- Try setting `DEBUG=True` temporarily to see the error
- Verify ALLOWED_HOSTS matches your exact URL (case-sensitive)

---

## Quick Test Commands (in Render Shell):

1. Go to Render → Your Service → **Shell** tab
2. Run:
   ```bash
   python manage.py shell
   ```
3. Then in Python shell:
   ```python
   from django.conf import settings
   print("ALLOWED_HOSTS:", settings.ALLOWED_HOSTS)
   print("DEBUG:", settings.DEBUG)
   ```

This will show you what Django actually sees.

---

## Still Not Working?

Share the error message from Render logs. The logs will tell us exactly what's wrong!

