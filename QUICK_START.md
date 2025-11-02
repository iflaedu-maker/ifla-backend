# 🚀 Quick Start: Deploy to Production in 30 Minutes

## TL;DR - Fast Deployment Steps

1. **Generate Secret Key**:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
   Copy the output!

2. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Ready for production"
   # Create repo on GitHub, then:
   git remote add origin https://github.com/YOUR_USERNAME/ifla-backend.git
   git push -u origin main
   ```

3. **Sign up on Render.com** (use GitHub account)

4. **Create PostgreSQL Database**:
   - Click "New +" → PostgreSQL
   - Name: `ifla-database`
   - Plan: Free
   - Copy the Internal Database URL

5. **Create Web Service**:
   - Click "New +" → Web Service
   - Connect your GitHub repo
   - Settings:
     - Build Command: `chmod +x build.sh && ./build.sh`
     - Start Command: `gunicorn ifla_backend.wsgi:application`
     - Plan: Free

6. **Add Environment Variables** (see full list below)

7. **Link Database** → Select your `ifla-database`

8. **Deploy!** → Click "Create Web Service"

9. **After deployment**: Go to Shell tab and run:
   ```bash
   python manage.py createsuperuser
   ```

---

## Essential Environment Variables

Add these in Render → Your Web Service → Environment:

| Variable | Value |
|----------|-------|
| `SECRET_KEY` | (paste the key from step 1) |
| `DEBUG` | `False` |
| `ENVIRONMENT` | `production` |
| `ALLOWED_HOSTS` | `your-app.onrender.com` |
| `EMAIL_HOST_USER` | your-email@gmail.com |
| `EMAIL_HOST_PASSWORD` | (Gmail app password) |
| `GOOGLE_OAUTH2_CLIENT_ID` | (your Google client ID) |
| `GOOGLE_OAUTH2_CLIENT_SECRET` | (your Google secret) |
| `GOOGLE_OAUTH2_REDIRECT_URI` | `https://your-app.onrender.com/api/auth/google/callback/` |
| `RAZORPAY_KEY_ID` | (your Razorpay key) |
| `RAZORPAY_KEY_SECRET` | (your Razorpay secret) |
| `CORS_ALLOWED_ORIGINS` | `https://your-app.onrender.com` |
| `CSRF_TRUSTED_ORIGINS` | `https://your-app.onrender.com` |

**Note**: `DATABASE_URL` is auto-set when you link the database!

---

## Full Guide

For detailed instructions, see **PRODUCTION_DEPLOYMENT.md**

---

## Cost: FREE! 🎉

- Free tier works great for starting
- Upgrade later if needed ($7/month for always-on)

