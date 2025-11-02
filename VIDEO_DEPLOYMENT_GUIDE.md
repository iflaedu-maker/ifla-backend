# 🎥 Video Files Deployment Guide

## Videos in Your Application

Your application uses 2 video files:
1. **`88116-602317818_medium.mp4`** - Hero section video
2. **`BENTO1.mp4`** - Stats card video

## Current Setup

The videos are:
- ✅ Located in: `static/media/`
- ✅ Referenced in: `templates/index.html`
- ✅ Using Django static files: `{% static 'media/88116-602317818_medium.mp4' %}`

## How Static Files Work in Production

1. **During Build**: `python manage.py collectstatic` copies all files from `static/` to `staticfiles/`
2. **In Production**: WhiteNoise serves files from `staticfiles/`
3. **Videos**: Are included automatically when you run `collectstatic`

## Verify Videos Are Deployed

### Step 1: Check if Videos Are Collected

After deployment, videos should be available at:
- `https://ifla-backend-9svs.onrender.com/static/media/88116-602317818_medium.mp4`
- `https://ifla-backend-9svs.onrender.com/static/media/BENTO1.mp4`

### Step 2: Test in Browser

Visit your production site and check:
1. Home page loads
2. Hero section video plays (autoplay, muted, loop)
3. Stats section video card plays

### Step 3: Check Render Build Logs

In Render build logs, look for:
```
166 static files copied to '/opt/render/project/src/staticfiles'
```

This means videos were collected. If you see:
```
static files copied...
```

It means all static files (including videos) were copied.

---

## If Videos Don't Load

### Issue 1: Videos Not in Git

**Check:**
1. Are videos in `static/media/` folder?
2. Are they committed to Git?
3. Are they pushed to GitHub?

**Fix:**
```bash
git add static/media/*.mp4
git commit -m "Add video files"
git push origin main
```

### Issue 2: Videos Too Large

**Problem**: Large video files (>10MB) can slow down deployment.

**Solutions**:
1. **Optimize videos**: Compress them using tools like HandBrake
2. **Use CDN**: Upload to Cloudinary, AWS S3, or similar
3. **Keep as-is**: If under 20MB each, they should work fine

### Issue 3: Videos Not Loading After Deployment

**Check Render Logs**:
- Look for errors related to static files
- Check if `collectstatic` completed successfully

**Manual Check**:
- Try accessing video URL directly:
  `https://your-app.onrender.com/static/media/88116-602317818_medium.mp4`

---

## Video File Locations

### Development:
- Videos in: `static/media/`
- Accessed via: `{% static 'media/filename.mp4' %}`

### Production (After collectstatic):
- Videos copied to: `staticfiles/media/`
- Served by WhiteNoise from: `/static/media/filename.mp4`

---

## File Sizes (Check)

Run this to check video sizes:
```bash
ls -lh static/media/*.mp4
```

**Recommended:**
- Keep videos under 10MB each for faster loading
- Use MP4 format (already correct)
- Consider compressing if over 20MB

---

## Alternative: Use Cloud Storage (For Large Videos)

If videos are very large, consider uploading to:
- **Cloudinary** (free tier: 25GB)
- **AWS S3** (free tier: 5GB for 12 months)
- **Google Cloud Storage**

Then update templates to use URLs:
```html
<source src="https://res.cloudinary.com/your-cloud/video/upload/v123/video.mp4" type="video/mp4">
```

---

## Current Status

✅ Videos are in `static/media/` folder
✅ Templates reference them correctly
✅ `collectstatic` will include them automatically
✅ WhiteNoise will serve them in production

**Just deploy and videos should work!**

---

## Verify After Deployment

1. Visit: `https://ifla-backend-9svs.onrender.com`
2. Check browser console (F12) for any 404 errors on video files
3. Videos should autoplay (muted, loop) on the home page

If videos don't load, check:
- Browser console for errors
- Network tab to see if files are loading
- Render logs for static file collection errors

