# 🔧 Troubleshooting Deployment Errors

## Common Error: "This error originates from a subprocess, and is likely not a problem with pip"

This error usually means a package failed to install. Here's how to fix it:

---

## Solution 1: Update build.sh (Most Common Fix)

The build script has been updated to handle this better. Make sure you have the latest version:

**The updated `build.sh` now:**
- Upgrades pip, setuptools, and wheel first
- Uses `--no-cache-dir` to avoid cached issues
- Provides better error messages

**If you still get errors, try this alternative:**

```bash
#!/usr/bin/env bash
set -o errexit

echo "Upgrading pip and tools..."
pip install --upgrade pip setuptools wheel

echo "Installing dependencies..."
pip install --no-cache-dir \
    Django==4.2.7 \
    djangorestframework==3.14.0 \
    django-cors-headers==4.3.1 \
    Pillow==10.1.0 \
    razorpay==1.4.2 \
    reportlab==4.0.7 \
    requests==2.31.0 \
    python-dotenv==1.0.0 \
    gunicorn==21.2.0 \
    whitenoise==6.6.0 \
    psycopg2-binary==2.9.9 \
    dj-database-url==2.1.0

echo "Collecting static files..."
python manage.py collectstatic --noinput || true

echo "Running migrations..."
python manage.py migrate --noinput

echo "Build completed!"
```

---

## Solution 2: Check Specific Package Errors

The error often comes from specific packages. Check Render logs to see which one:

### If it's `psycopg2-binary`:
This package is already `psycopg2-binary` (the binary version), so it should work. If it fails:
- Make sure you're using `psycopg2-binary==2.9.9` (not `psycopg2`)
- The binary version doesn't need PostgreSQL development libraries

### If it's `Pillow`:
Pillow might need system libraries. On Render, this should work automatically, but if it fails:
- Try updating to `Pillow==10.2.0` or latest
- Or remove version pin and let it install latest: `Pillow`

### If it's `reportlab`:
Reportlab is usually fine, but if errors occur:
- Try: `reportlab` (without version)
- Or: `reportlab==4.1.0` (newer version)

---

## Solution 3: Update requirements.txt (Alternative)

If specific packages keep failing, you can try more flexible versions:

```txt
Django>=4.2,<5.0
djangorestframework>=3.14.0
django-cors-headers>=4.3.0
Pillow>=10.0.0
razorpay>=1.4.0
reportlab>=4.0.0
requests>=2.31.0
python-dotenv>=1.0.0
gunicorn>=21.2.0
whitenoise>=6.6.0
psycopg2-binary>=2.9.0
dj-database-url>=2.1.0
```

**Note:** Using `>=` allows pip to install compatible versions if exact versions fail.

---

## Solution 4: Check Render Logs for Details

1. Go to your Render dashboard
2. Click on your web service
3. Go to **"Logs"** tab
4. Look for the specific error message
5. The error will show which package failed

**Common patterns in errors:**
- `error: command 'gcc' failed` → Build tools issue (rare on Render)
- `Failed building wheel for X` → Package build issue
- `No module named 'X'` → Package not installed

---

## Solution 5: Try Installing Packages One by One

If you want to identify the exact problem, modify `build.sh`:

```bash
#!/usr/bin/env bash
set -o errexit

pip install --upgrade pip setuptools wheel

# Install core packages first
pip install Django==4.2.7
pip install djangorestframework==3.14.0
pip install django-cors-headers==4.3.1

# Install database
pip install psycopg2-binary==2.9.9
pip install dj-database-url==2.1.0

# Install other packages
pip install Pillow==10.1.0
pip install razorpay==1.4.2
pip install reportlab==4.0.7
pip install requests==2.31.0
pip install python-dotenv==1.0.0

# Install production packages
pip install gunicorn==21.2.0
pip install whitenoise==6.6.0

python manage.py collectstatic --noinput || true
python manage.py migrate --noinput
```

This way, you'll see exactly which package fails.

---

## Solution 6: Check Python Version

Make sure `runtime.txt` has a compatible version:

```txt
python-3.11.7
```

Or try:
```txt
python-3.11.8
```

Or:
```txt
python-3.12.0
```

---

## Solution 7: Alternative - Use Render's Auto-Detect

If build script keeps failing, you can let Render auto-detect:

1. In Render dashboard → Your service → Settings
2. Remove or comment out the Build Command
3. Render will auto-detect Django and run:
   - `pip install -r requirements.txt`
   - `python manage.py collectstatic`
   - `python manage.py migrate`

**But you still need to set Start Command:** `gunicorn ifla_backend.wsgi:application`

---

## Most Likely Causes (In Order)

1. **pip/setuptools not upgraded** - Fixed in updated build.sh
2. **psycopg2-binary build issue** - Shouldn't happen with binary version
3. **Pillow system dependencies** - Rare on Render
4. **Network/timeout issues** - Try again, or use `--no-cache-dir`
5. **Python version mismatch** - Check runtime.txt

---

## Quick Fix Checklist

- [ ] Updated `build.sh` with the new version
- [ ] Checked Render logs for specific package error
- [ ] Verified `runtime.txt` has Python 3.11.x
- [ ] Tried rebuilding the service
- [ ] Checked that `requirements.txt` has correct package names

---

## Still Not Working?

1. **Copy the FULL error message** from Render logs
2. **Check which package** is mentioned in the error
3. **Share the error** and I can provide a specific fix

---

## Pro Tip: Use Render Shell to Debug

1. In Render dashboard → Your service
2. Click **"Shell"** tab
3. Run commands manually:
   ```bash
   pip install --upgrade pip
   pip install psycopg2-binary
   ```
4. See the actual error message

This helps identify the exact problem!

