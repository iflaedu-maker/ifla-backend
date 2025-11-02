# 🔧 Fix: Server Error (500)

A 500 error means the server is running but something is crashing. Let's fix it!

## Step 1: Check Render Logs

1. Go to Render Dashboard → Your Service → **"Logs"** tab
2. Look for **RED error messages** (Python tracebacks)
3. **Copy the error message** - it will tell us exactly what's wrong

Common errors you might see:

### Error 1: Database Connection Issues
```
django.db.utils.OperationalError: could not connect to server
```
**Fix**: Make sure your database is linked to the web service

### Error 2: Missing Environment Variables
```
KeyError: 'SECRET_KEY'
```
**Fix**: Add missing environment variables

### Error 3: Migration Issues
```
django.db.utils.ProgrammingError: relation does not exist
```
**Fix**: Run migrations

### Error 4: Import Errors
```
ModuleNotFoundError: No module named 'xxx'
```
**Fix**: Missing dependency in requirements.txt

---

## Step 2: Verify Environment Variables

Make sure these are set in Render:

### Required:
- ✅ `SECRET_KEY` - Your Django secret key
- ✅ `DEBUG` - Set to `True` temporarily to see errors, then `False` for production
- ✅ `ENVIRONMENT` - Set to `production`
- ✅ `ALLOWED_HOSTS` - Your domain or `*` for testing
- ✅ `DATABASE_URL` - Should be auto-set when database is linked

### Important:
- ✅ Make sure your **PostgreSQL database is linked** to your web service
- ✅ Check that database is **running** (not paused)

---

## Step 3: Enable DEBUG to See Detailed Errors

1. Go to Render → Settings → Environment Variables
2. Set:
   - `DEBUG` = `True`
3. Save and wait for redeploy
4. Visit your site - you'll see the detailed error page

**⚠️ Remember**: Set `DEBUG=False` after fixing!

---

## Step 4: Common Fixes

### Fix 1: Database Not Connected

1. Go to Render → Your Web Service → **Settings**
2. Scroll to **"Links"** section
3. Make sure your database (`ifla-database`) is listed
4. If not, click **"Link Database"** and select it
5. Redeploy

### Fix 2: Missing Migrations

1. Go to Render → Your Service → **Shell** tab
2. Run:
   ```bash
   python manage.py migrate
   ```

### Fix 3: Missing SECRET_KEY

1. Generate a new secret key:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
2. Copy the output
3. In Render → Settings → Environment Variables
4. Set `SECRET_KEY` to the copied value

### Fix 4: Create Superuser (if needed)

1. Go to Render → Your Service → **Shell** tab
2. Run:
   ```bash
   python manage.py createsuperuser
   ```
3. Follow prompts

---

## Step 5: Test Database Connection

In Render Shell:
```bash
python manage.py shell
```

Then in Python:
```python
from django.db import connection
cursor = connection.cursor()
cursor.execute("SELECT 1")
print("Database connected!")
```

If you see an error, the database isn't connected properly.

---

## Quick Checklist:

- [ ] Database is linked to web service
- [ ] Database is running (not paused)
- [ ] `DATABASE_URL` environment variable exists (should be auto-set)
- [ ] `SECRET_KEY` is set
- [ ] `DEBUG=True` temporarily to see errors
- [ ] Check Render logs for specific error
- [ ] Run migrations if needed

---

## Share the Error:

**Most Important**: Copy the error from Render logs and share it. That will tell us exactly what's wrong!

To find the error:
1. Render → Your Service → **Logs**
2. Look for lines with red text or "ERROR"
3. Copy the full error message (especially the traceback)
4. Share it here!

