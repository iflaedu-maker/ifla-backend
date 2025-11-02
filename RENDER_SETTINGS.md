# 🔧 Render Settings Configuration

## Critical Settings to Configure in Render Dashboard

### 1. Python Version (IMPORTANT!)

**Why**: Your `runtime.txt` specifies Python 3.11.7, but Render might default to 3.13.4 which causes Pillow build errors.

**How to Fix**:

1. Go to your Render Web Service
2. Click **"Settings"** tab
3. Scroll down to **"Environment Variables"**
4. Click **"Add Environment Variable"**
5. Add:
   - **Key**: `PYTHON_VERSION`
   - **Value**: `3.11.7`
6. Save

**OR** in the service settings, look for **"Python Version"** field and set it to `3.11.7`

---

### 2. Build Command (FIX THIS!)

**Current (Wrong)**: `chmod +x build.sh && ./build.sh`

**Should be**: `bash build.sh`

**How to Fix**:

1. Go to your Render Web Service
2. Click **"Settings"** tab
3. Find **"Build Command"** field
4. Replace with: `bash build.sh`
5. **DO NOT** include backticks or quotes
6. Save

---

### 3. Verify Settings

Make sure these are set correctly:

- ✅ **Python Version**: `3.11.7`
- ✅ **Build Command**: `bash build.sh` (no backticks!)
- ✅ **Start Command**: `gunicorn ifla_backend.wsgi:application`
- ✅ **Root Directory**: (leave empty)
- ✅ **Branch**: `main`

---

After updating these settings, click **"Manual Deploy"** → **"Clear build cache & deploy"**

