# 🐛 Debug Server Error (500) - Step by Step

## ✅ Progress Made!
- **400 Error** → FIXED! ✅
- **500 Error** → Now debugging this

A 500 error means the server is running but something is crashing. Let's find and fix it!

---

## Step 1: Enable DEBUG Mode (See Actual Error)

**This is the MOST IMPORTANT step!**

1. Go to **Render Dashboard** → Your `ifla-backend` service
2. Click **"Settings"** tab
3. Scroll to **"Environment Variables"**
4. Find `DEBUG` variable
5. Change it to: `True`
6. **Save**
7. Wait for auto-redeploy (2-3 minutes)
8. Visit your site: `https://ifla-backend-9svs.onrender.com`

**Now you'll see the ACTUAL error message instead of "Server Error (500)"!**

The error page will show:
- ❌ What went wrong
- 📍 Where it crashed (file and line number)
- 📋 Full error traceback

---

## Step 2: Check Common Issues

### Issue 1: Database Not Connected

**Symptoms:**
- Error: `django.db.utils.OperationalError`
- Error: `relation does not exist`
- Error: `could not connect to server`

**Fix:**
1. Go to Render → Your Web Service → **Settings**
2. Scroll to **"Links"** section
3. Make sure `ifla-database` is listed and **linked**
4. If NOT linked:
   - Click **"Link Database"**
   - Select your `ifla-database`
   - Save
5. Redeploy your web service

---

### Issue 2: Missing Environment Variables

**Symptoms:**
- Error mentioning `SECRET_KEY`
- Error about missing config

**Fix:**
Make sure these are set in Render → Settings → Environment Variables:

**Required:**
- ✅ `SECRET_KEY` = (your generated secret key)
- ✅ `DEBUG` = `True` (for debugging) or `False` (for production)
- ✅ `ENVIRONMENT` = `production`
- ✅ `ALLOWED_HOSTS` = `ifla-backend-9svs.onrender.com` or `*`
- ✅ `DATABASE_URL` = (should auto-set when database is linked)

---

### Issue 3: Database Migrations Not Run

**Symptoms:**
- Error: `relation "xxx" does not exist`
- Error: `no such table`

**Fix:**
1. Go to Render → Your Service → **"Shell"** tab
2. Run:
   ```bash
   python manage.py migrate
   ```
3. This will create all database tables

---

### Issue 4: Missing Dependencies

**Symptoms:**
- Error: `ModuleNotFoundError: No module named 'xxx'`
- Error: `ImportError`

**Fix:**
1. Check `requirements.txt` includes the missing module
2. If missing, add it
3. Push to GitHub
4. Render will auto-redeploy

---

## Step 3: Quick Diagnostic Commands

Run these in Render → Shell to check:

### Test Database Connection:
```bash
python manage.py shell
```
Then in Python:
```python
from django.db import connection
cursor = connection.cursor()
cursor.execute("SELECT 1")
print("✅ Database connected!")
```

If error: Database not connected properly.

---

### Check Environment Variables:
```bash
python manage.py shell
```
Then:
```python
import os
from django.conf import settings
print("DEBUG:", settings.DEBUG)
print("ALLOWED_HOSTS:", settings.ALLOWED_HOSTS)
print("DATABASE_URL exists:", bool(os.getenv('DATABASE_URL')))
print("SECRET_KEY exists:", bool(os.getenv('SECRET_KEY')))
```

---

## Step 4: Most Common 500 Errors & Fixes

### Error: "DisallowedHost"
**Already fixed!** But if you see it:
- Set `ALLOWED_HOSTS=*` temporarily

### Error: Database Connection Failed
**Fix:**
- Link database to web service
- Check database is running (not paused)

### Error: Secret Key Missing
**Fix:**
- Generate: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- Add to Render → Settings → Environment Variables

### Error: No Such Table
**Fix:**
- Run: `python manage.py migrate` in Render Shell

### Error: Template Not Found
**Fix:**
- Check `TEMPLATES` setting in `settings.py`
- Verify template files exist

---

## Step 5: Share the Error!

**After enabling DEBUG=True**, copy the error message and share it. It will tell us exactly what's wrong!

The error will look like:
```
Traceback (most recent call last):
  File "...", line XX, in ...
    [error details]
```

---

## Quick Fix Checklist:

- [ ] Set `DEBUG=True` in Render
- [ ] Wait for redeploy
- [ ] Visit site and see actual error
- [ ] Database is linked to web service
- [ ] `SECRET_KEY` is set
- [ ] `DATABASE_URL` exists (auto-set)
- [ ] Run migrations if needed
- [ ] Copy error message from the page

---

## After Fixing:

1. Once error is fixed, set `DEBUG=False` for production
2. Verify site works properly
3. Test all features:
   - Home page loads
   - Login/signup works
   - Admin panel works

---

**Next Step**: Enable `DEBUG=True` in Render, then share the error message you see!

