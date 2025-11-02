# ✅ Pre-Deployment Checklist

Use this checklist before deploying to ensure everything is ready.

## Code Preparation

- [x] ✅ Production dependencies added (`gunicorn`, `whitenoise`, `psycopg2-binary`, `dj-database-url`)
- [x] ✅ `settings.py` updated for production (PostgreSQL, security, environment detection)
- [x] ✅ `build.sh` created for deployment
- [x] ✅ `runtime.txt` specified Python version
- [x] ✅ `Procfile` created for web service

## Before Deployment

- [ ] Generate `SECRET_KEY`:
  ```bash
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```

- [ ] Code committed to Git
- [ ] Repository pushed to GitHub
- [ ] Render.com account created

## Environment Variables to Set

### Core Django
- [ ] `SECRET_KEY` (required)
- [ ] `DEBUG=False` (required)
- [ ] `ENVIRONMENT=production` (required)
- [ ] `ALLOWED_HOSTS` (required - your Render domain)

### Database
- [ ] `DATABASE_URL` (auto-set when linking database in Render)

### Email
- [ ] `EMAIL_HOST=smtp.gmail.com`
- [ ] `EMAIL_PORT=587`
- [ ] `EMAIL_USE_TLS=True`
- [ ] `EMAIL_HOST_USER` (your Gmail)
- [ ] `EMAIL_HOST_PASSWORD` (Gmail app password)
- [ ] `DEFAULT_FROM_EMAIL` (your Gmail)

### Google OAuth
- [ ] `GOOGLE_OAUTH2_CLIENT_ID`
- [ ] `GOOGLE_OAUTH2_CLIENT_SECRET`
- [ ] `GOOGLE_OAUTH2_REDIRECT_URI` (must match production URL)

### Razorpay
- [ ] `RAZORPAY_KEY_ID`
- [ ] `RAZORPAY_KEY_SECRET`

### CORS/CSRF
- [ ] `CORS_ALLOWED_ORIGINS` (your production URL)
- [ ] `CSRF_TRUSTED_ORIGINS` (your production URL)

## After Deployment

- [ ] Verify site loads at your Render URL
- [ ] Create superuser account (in Render Shell)
- [ ] Test login/signup
- [ ] Test Google OAuth (update redirect URI in Google Console)
- [ ] Test enrollment form
- [ ] Test payment flow
- [ ] Verify admin panel works (`/admin/`)
- [ ] Check static files load correctly
- [ ] Test email sending (contact form, OTP)

## Post-Deployment Updates

- [ ] Update Google OAuth redirect URI to production URL
- [ ] Update Razorpay webhook URL (if using webhooks)
- [ ] Set up custom domain (optional)
- [ ] Configure email notifications
- [ ] Test all critical user flows

## Monitoring

- [ ] Check Render logs for any errors
- [ ] Monitor database usage (free tier: 1GB limit)
- [ ] Set up uptime monitoring (optional)

---

**Ready to deploy?** Follow `PRODUCTION_DEPLOYMENT.md` for step-by-step instructions!

