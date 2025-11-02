# Production Deployment Guide - Step by Step

This guide will help you deploy your IFLA Django application to **Render.com** (free tier available, all-in-one platform).

## Why Render.com?
- ✅ **Free tier available** for web services and PostgreSQL database
- ✅ **Everything in one platform** - hosting, database, SSL
- ✅ **Easy to use** - beginner friendly
- ✅ **Automatic SSL/HTTPS** - secure by default
- ✅ **Auto-deploy from Git** - push code, it deploys automatically
- ✅ **Scalable** - can upgrade as you grow

## Prerequisites

1. **GitHub Account** (free)
2. **Render.com Account** (free to sign up)
3. **Git installed** on your computer

---

## Step 1: Prepare Your Code

### 1.1 Generate a Secret Key

Run this command to generate a secure secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output - you'll need it later.

### 1.2 Create a .gitignore file (if not exists)

Make sure `.env` is in `.gitignore` (should already be there).

### 1.3 Commit Your Code to Git

```bash
# If you haven't initialized git yet
git init
git add .
git commit -m "Initial commit - ready for production"
```

---

## Step 2: Push to GitHub

### 2.1 Create a GitHub Repository

1. Go to [GitHub.com](https://github.com)
2. Click "New" to create a new repository
3. Name it something like `ifla-backend`
4. **Don't** initialize with README (you already have code)
5. Click "Create repository"

### 2.2 Push Your Code

GitHub will show you commands. Run these in your project folder:

```bash
git remote add origin https://github.com/YOUR_USERNAME/ifla-backend.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

---

## Step 3: Create Render Account

1. Go to [Render.com](https://render.com)
2. Click "Get Started for Free"
3. Sign up with your GitHub account (easiest option)
4. Verify your email if needed

---

## Step 4: Create PostgreSQL Database on Render

### 4.1 Create Database

1. In Render dashboard, click **"New +"**
2. Select **"PostgreSQL"**
3. Configure:
   - **Name**: `ifla-database`
   - **Database**: `ifla_db`
   - **User**: `ifla_user`
   - **Plan**: **Free** (1GB storage, 90-day retention)
   - **Region**: **Choose based on your audience:**
     - 🇮🇳 **For Indian audience**: Choose **"Mumbai (India)"** or **"Singapore"** (closest to India, better latency)
     - 🇺🇸 **For US audience**: Choose **"Oregon (US West)"** or **"Ohio (US East)"**
     - 🇪🇺 **For European audience**: Choose **"Frankfurt (EU)"**
     - 🌍 **Global/Mixed**: Choose **"Singapore"** (good middle ground)
4. Click **"Create Database"**

**💡 Tip**: Choose **Singapore** or **Mumbai** for best performance for Indian users!

### 4.2 Save Database Connection String

1. Once created, click on your database
2. Find the **"Internal Database URL"** (starts with `postgresql://`)
3. **Copy it** - you'll need it if not using auto-link

**Note**: Render will auto-link the database if you use `render.yaml`, but manual setup is also fine.

---

## Step 5: Deploy Web Service on Render

### 5.1 Create Web Service

1. In Render dashboard, click **"New +"**
2. Select **"Web Service"**
3. Connect your GitHub repository:
   - Click **"Connect GitHub"** if not connected
   - Select your `ifla-backend` repository
4. Configure the service:
   - **Name**: `ifla-backend`
   - **Region**: Same as database
   - **Branch**: `main`
   - **Root Directory**: (leave empty - root is fine)
   - **Environment**: `Python 3`
   - **Build Command**: `bash build.sh`
     - **OR** if that doesn't work: `chmod +x build.sh && ./build.sh`
     - **IMPORTANT**: Do NOT include backticks (`) around the command - just paste it as shown
   - **Start Command**: `gunicorn ifla_backend.wsgi:application`
   - **Plan**: **Free** (or Starter for $7/month with more resources)

### 5.2 Add Environment Variables

Scroll down to **"Environment Variables"** and add these:

#### Required Variables:

```
SECRET_KEY
```
**Value**: Paste the secret key you generated in Step 1.1

```
DEBUG
```
**Value**: `False`

```
ENVIRONMENT
```
**Value**: `production`

```
ALLOWED_HOSTS
```
**Value**: `your-app-name.onrender.com,www.your-app-name.onrender.com`
(Replace `your-app-name` with your actual Render service name)

#### Database (if not auto-linked):

```
DATABASE_URL
```
**Value**: Paste the Internal Database URL from Step 4.2

#### Email Configuration:

```
EMAIL_HOST
```
**Value**: `smtp.gmail.com`

```
EMAIL_PORT
```
**Value**: `587`

```
EMAIL_USE_TLS
```
**Value**: `True`

```
EMAIL_HOST_USER
```
**Value**: Your Gmail address

```
EMAIL_HOST_PASSWORD
```
**Value**: Gmail App Password (see Email Setup below)

```
DEFAULT_FROM_EMAIL
```
**Value**: Your Gmail address

#### Google OAuth:

```
GOOGLE_OAUTH2_CLIENT_ID
```
**Value**: Your Google OAuth Client ID

```
GOOGLE_OAUTH2_CLIENT_SECRET
```
**Value**: Your Google OAuth Client Secret

```
GOOGLE_OAUTH2_REDIRECT_URI
```
**Value**: `https://your-app-name.onrender.com/api/auth/google/callback/`
(Replace with your actual Render URL)

#### Razorpay:

```
RAZORPAY_KEY_ID
```
**Value**: Your Razorpay Key ID

```
RAZORPAY_KEY_SECRET
```
**Value**: Your Razorpay Key Secret

#### CORS & CSRF:

```
CORS_ALLOWED_ORIGINS
```
**Value**: `https://your-app-name.onrender.com,https://www.your-app-name.onrender.com`

```
CSRF_TRUSTED_ORIGINS
```
**Value**: `https://your-app-name.onrender.com,https://www.your-app-name.onrender.com`

### 5.3 Link Database (if not auto-linked)

1. Scroll to **"Links"** section
2. Click **"Link Database"**
3. Select your `ifla-database`
4. Render will automatically set `DATABASE_URL`

### 5.4 Deploy

1. Click **"Create Web Service"**
2. Render will start building and deploying
3. This takes 5-10 minutes for first deployment
4. Watch the logs to see progress

---

## Step 6: Update Google OAuth Redirect URI

After deployment, you'll get a URL like: `https://your-app-name.onrender.com`

1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Edit your OAuth 2.0 credentials
3. Add to **"Authorized redirect URIs"**:
   ```
   https://your-app-name.onrender.com/api/auth/google/callback/
   ```
4. Save

---

## Step 7: Update Razorpay Webhook (if using)

1. Go to [Razorpay Dashboard](https://dashboard.razorpay.com)
2. Navigate to **Webhooks**
3. Add webhook URL:
   ```
   https://your-app-name.onrender.com/api/courses/payment/webhook/
   ```

---

## Step 8: Run Initial Setup

After first deployment succeeds, you may need to:

### 8.1 Create Superuser

Render provides a **Shell** feature:
1. Go to your web service
2. Click **"Shell"** tab
3. Run:
   ```bash
   python manage.py createsuperuser
   ```
4. Follow prompts to create admin account

### 8.2 Verify Database Migration

Migrations should run automatically from `build.sh`, but verify:
1. In Shell, run:
   ```bash
   python manage.py migrate
   ```

---

## Step 9: Test Your Deployment

1. Visit: `https://your-app-name.onrender.com`
2. Test:
   - Home page loads
   - Login/Signup works
   - Google OAuth works
   - Enrollment form works
   - Payment works
   - Admin panel: `https://your-app-name.onrender.com/admin/`

---

## Step 10: Set Up Custom Domain (Optional)

If you have a custom domain:

1. In Render, go to your web service
2. Click **"Settings"**
3. Scroll to **"Custom Domains"**
4. Add your domain
5. Follow DNS configuration instructions
6. Update environment variables:
   - `ALLOWED_HOSTS`: Add your domain
   - `CORS_ALLOWED_ORIGINS`: Add your domain
   - `CSRF_TRUSTED_ORIGINS`: Add your domain
7. Update Google OAuth redirect URI to include your domain

---

## Email Setup (Gmail App Password)

For production emails, you need a Gmail App Password:

1. Go to [Google Account](https://myaccount.google.com)
2. **Security** → **2-Step Verification** (enable if not enabled)
3. **App passwords** → Generate new app password
4. Select **Mail** and **Other (Custom name)**
5. Name it: "IFLA Django"
6. Copy the 16-character password
7. Use this in `EMAIL_HOST_PASSWORD` environment variable

---

## Important: Media Files Storage

**⚠️ Note**: Render's free tier uses ephemeral file systems. Uploaded files (media/) will be lost on restarts.

**For Production Media Files, you have options:**

1. **Use Cloud Storage** (Recommended for production):
   - **AWS S3** (free tier: 5GB for 12 months, then ~$0.023/GB/month)
   - **Cloudinary** (free tier: 25GB storage, 25GB bandwidth/month)
   - **DigitalOcean Spaces** ($5/month for 250GB)
   - Update `settings.py` to use django-storages

2. **Use Render Disk** (if upgrading to paid plan):
   - Upgrade to Starter plan ($7/month)
   - Persistent disk storage available

3. **Current Setup** (for testing):
   - Files persist until deployment restart
   - Fine for development/testing
   - Not suitable for production with user uploads

**Recommendation**: For now, deploy as-is. When ready for production with file uploads, add cloud storage.

---

## Troubleshooting

### Build Fails

- Check logs in Render dashboard
- Ensure all dependencies in `requirements.txt`
- Verify Python version in `runtime.txt` matches Render

### Database Connection Issues

- Verify `DATABASE_URL` is set correctly
- Check database is running in Render
- Ensure database is linked to web service

### Static Files Not Loading

- Check `build.sh` runs `collectstatic`
- Verify `STATIC_ROOT` in settings
- Check WhiteNoise middleware is installed

### 500 Errors

- Check logs in Render dashboard
- Verify all environment variables are set
- Check `DEBUG=False` in production
- Verify `SECRET_KEY` is set

### CORS/CSRF Errors

- Verify `CORS_ALLOWED_ORIGINS` includes your domain
- Verify `CSRF_TRUSTED_ORIGINS` includes your domain
- Check URLs use HTTPS in production

---

## Cost Breakdown

### Free Tier (Recommended for Start)
- **Web Service**: Free (with limitations: spins down after 15 min inactivity)
- **PostgreSQL**: Free (1GB storage, 90-day backup retention)
- **Total**: **$0/month**

### Starter Plan (If You Need Always-On)
- **Web Service**: $7/month (always-on, better performance)
- **PostgreSQL**: Free (or upgrade to $7/month for more storage)
- **Total**: **$7-14/month**

---

## Next Steps After Deployment

1. ✅ Test all features
2. ✅ Set up monitoring (Render provides basic logs)
3. ✅ Configure backups (Render handles this)
4. ✅ Set up custom domain
5. ✅ Enable email notifications
6. ✅ Regular updates: just push to GitHub, Render auto-deploys

---

## Support

- **Render Docs**: https://render.com/docs
- **Django Deployment**: https://docs.djangoproject.com/en/4.2/howto/deployment/
- **Render Support**: Available in dashboard

---

## Quick Reference: Environment Variables Checklist

Copy this checklist and check off as you add each:

- [ ] `SECRET_KEY`
- [ ] `DEBUG=False`
- [ ] `ENVIRONMENT=production`
- [ ] `ALLOWED_HOSTS`
- [ ] `DATABASE_URL` (auto-set if linked)
- [ ] `EMAIL_HOST`
- [ ] `EMAIL_PORT`
- [ ] `EMAIL_USE_TLS`
- [ ] `EMAIL_HOST_USER`
- [ ] `EMAIL_HOST_PASSWORD`
- [ ] `DEFAULT_FROM_EMAIL`
- [ ] `GOOGLE_OAUTH2_CLIENT_ID`
- [ ] `GOOGLE_OAUTH2_CLIENT_SECRET`
- [ ] `GOOGLE_OAUTH2_REDIRECT_URI`
- [ ] `RAZORPAY_KEY_ID`
- [ ] `RAZORPAY_KEY_SECRET`
- [ ] `CORS_ALLOWED_ORIGINS`
- [ ] `CSRF_TRUSTED_ORIGINS`

---

**You're all set! Your app should now be live on Render! 🚀**

