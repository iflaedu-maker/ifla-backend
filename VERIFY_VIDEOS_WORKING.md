# ✅ Verify Videos Are Working in Production

## Quick Check

After deployment, test if videos are working:

1. **Visit your site**: `https://ifla-backend-9svs.onrender.com`
2. **Check home page**: Videos should autoplay automatically
3. **Open browser console** (F12) → **Network** tab
4. **Refresh page**
5. **Look for**: `88116-602317818_medium.mp4` and `BENTO1.mp4`

### Expected Behavior:
- ✅ Videos should load (status 200)
- ✅ Videos should autoplay (muted, loop)
- ✅ No 404 errors in console

---

## If Videos Don't Work

### Step 1: Check if Videos Are Being Served

Try accessing videos directly:
- `https://ifla-backend-9svs.onrender.com/static/media/88116-602317818_medium.mp4`
- `https://ifla-backend-9svs.onrender.com/static/media/BENTO1.mp4`

**If you get 404:**
- Videos weren't collected during build
- Check Render build logs for `collectstatic` errors

**If you get 200:**
- Videos are served correctly
- Issue might be with template/HTML

### Step 2: Check Browser Console

Open browser console (F12) and look for:
- ❌ `404 Not Found` for video files → Static files issue
- ❌ `CORS error` → CORS configuration issue
- ❌ `MIME type error` → Server configuration issue

### Step 3: Check Render Build Logs

In Render → Your Service → **Logs**:
Look for:
```
166 static files copied to '/opt/render/project/src/staticfiles'
```

Or:
```
Collecting static files...
static files copied
```

If you see errors about videos, they might be too large or missing.

---

## Common Issues & Fixes

### Issue 1: Videos Not Loading (404)

**Cause**: Videos not collected during build

**Fix**:
1. Check that videos exist in `static/media/` folder
2. Verify they're committed to Git
3. Check Render build logs for `collectstatic` output
4. Redeploy if needed

### Issue 2: Videos Load But Don't Autoplay

**Cause**: Browser autoplay policies

**Fix**: 
- This is normal! Modern browsers may block autoplay
- Videos are set to `muted` and `autoplay` which should work
- Check browser settings if they still don't autoplay

### Issue 3: CORS Errors

**Cause**: CORS settings blocking static files (unlikely)

**Fix**: Already configured in `settings.py` - shouldn't be an issue

### Issue 4: Videos Too Large

**Problem**: Large videos slow down deployment and loading

**Solution**: 
- Videos should work even if large
- Consider compressing if over 50MB each
- WhiteNoise handles large files fine

---

## Verify Static Files Configuration

The setup is correct:
- ✅ `STATIC_URL = '/static/'`
- ✅ `STATIC_ROOT = BASE_DIR / 'staticfiles'`
- ✅ `STATICFILES_DIRS = [BASE_DIR / 'static']`
- ✅ WhiteNoise middleware configured
- ✅ `collectstatic` runs during build

---

## Expected File Structure After Build

```
project/
├── static/
│   └── media/
│       ├── 88116-602317818_medium.mp4
│       └── BENTO1.mp4
└── staticfiles/
    └── media/
        ├── 88116-602317818_medium.mp4
        └── BENTO1.mp4
```

WhiteNoise serves from `staticfiles/` in production.

---

## Test Videos Locally First

Before deploying, test locally:
```bash
python manage.py collectstatic
python manage.py runserver
```

Visit `http://localhost:8000` and verify videos work.

---

## Video File Requirements

✅ **Format**: MP4 (H.264 codec recommended)
✅ **Location**: `static/media/`
✅ **Template**: Uses `{% static 'media/filename.mp4' %}`
✅ **Size**: Any size (but keep reasonable for loading speed)

---

## After Deployment

Once deployed, videos should work exactly like localhost:
- ✅ Same autoplay behavior
- ✅ Same loop and muted settings
- ✅ Same visual appearance

If they don't, check the steps above!

