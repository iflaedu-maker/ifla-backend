# Email OTP Production Setup Guide

This guide will help you configure email sending for production so that OTP codes are sent via real emails instead of console output.

## Quick Setup Options

### Option 1: Gmail (Easiest - Good for Testing/Small Scale)

#### Step 1: Create Gmail App Password
1. Go to your Google Account: https://myaccount.google.com/
2. Click **Security** on the left sidebar
3. Enable **2-Step Verification** (if not already enabled)
4. Scroll down to **App passwords**
5. Click **App passwords**
6. Select app: **Mail**
7. Select device: **Other (Custom name)** and enter "IFLA Django"
8. Click **Generate**
9. **Copy the 16-character password** (you'll need this)

#### Step 2: Set Environment Variables
Set these environment variables on your production server:

**For Linux/Mac:**
```bash
export ENVIRONMENT=production
export EMAIL_HOST=smtp.gmail.com
export EMAIL_PORT=587
export EMAIL_USE_TLS=True
export EMAIL_HOST_USER=your-email@gmail.com
export EMAIL_HOST_PASSWORD=your-16-char-app-password
export DEFAULT_FROM_EMAIL=your-email@gmail.com
```

**For Windows (PowerShell):**
```powershell
$env:ENVIRONMENT="production"
$env:EMAIL_HOST="smtp.gmail.com"
$env:EMAIL_PORT="587"
$env:EMAIL_USE_TLS="True"
$env:EMAIL_HOST_USER="your-email@gmail.com"
$env:EMAIL_HOST_PASSWORD="your-16-char-app-password"
$env:DEFAULT_FROM_EMAIL="your-email@gmail.com"
```

**For Windows (.env file or IIS):**
Add to your `.env` file or set in IIS environment variables:
```
ENVIRONMENT=production
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-char-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

---

### Option 2: SendGrid (Recommended for Production)

SendGrid is a professional email service with a free tier (100 emails/day forever).

#### Step 1: Create SendGrid Account
1. Sign up at https://sendgrid.com/
2. Verify your email address
3. Complete account setup

#### Step 2: Create API Key
1. Go to **Settings** → **API Keys**
2. Click **Create API Key**
3. Name it "IFLA Django Email"
4. Select **Full Access** or **Mail Send** permission
5. Click **Create & View**
6. **Copy the API key** (you'll only see it once!)

#### Step 3: Set Environment Variables
```bash
export ENVIRONMENT=production
export EMAIL_HOST=smtp.sendgrid.net
export EMAIL_PORT=587
export EMAIL_USE_TLS=True
export EMAIL_HOST_USER=apikey
export EMAIL_HOST_PASSWORD=your-sendgrid-api-key
export DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

---

### Option 3: AWS SES (Best for Large Scale)

Amazon Simple Email Service is ideal for high-volume email sending.

#### Step 1: Set Up AWS SES
1. Sign in to AWS Console
2. Go to **Amazon SES** service
3. Verify your email address or domain
4. Move out of "Sandbox" mode (request production access if needed)

#### Step 2: Create SMTP Credentials
1. In SES, go to **SMTP Settings**
2. Click **Create SMTP Credentials**
3. Copy the **SMTP Username** and **SMTP Password**

#### Step 3: Set Environment Variables
```bash
export ENVIRONMENT=production
export EMAIL_HOST=email-smtp.us-east-1.amazonaws.com  # Use your region endpoint
export EMAIL_PORT=587
export EMAIL_USE_TLS=True
export EMAIL_HOST_USER=your-smtp-username
export EMAIL_HOST_PASSWORD=your-smtp-password
export DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

**Note**: Replace `us-east-1` with your AWS region (e.g., `eu-west-1`, `ap-south-1`)

---

## Deployment Methods

### Method 1: Using .env File (Recommended)

Create a `.env` file in your project root (same directory as `manage.py`):

```env
ENVIRONMENT=production
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

**Important**: Add `.env` to `.gitignore` to prevent committing secrets:
```
.env
```

### Method 2: Environment Variables in Hosting Platform

#### PythonAnywhere
1. Go to **Web** tab
2. Click on your web app
3. Scroll to **Environment variables**
4. Add each variable:
   - `ENVIRONMENT` = `production`
   - `EMAIL_HOST` = `smtp.gmail.com`
   - etc.

#### Heroku
```bash
heroku config:set ENVIRONMENT=production
heroku config:set EMAIL_HOST=smtp.gmail.com
heroku config:set EMAIL_PORT=587
heroku config:set EMAIL_USE_TLS=True
heroku config:set EMAIL_HOST_USER=your-email@gmail.com
heroku config:set EMAIL_HOST_PASSWORD=your-app-password
heroku config:set DEFAULT_FROM_EMAIL=your-email@gmail.com
```

#### AWS EC2 / Linux Server
Add to `/etc/environment` or create a startup script:
```bash
sudo nano /etc/environment
```

Add:
```
ENVIRONMENT=production
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

#### Windows IIS
1. Open **IIS Manager**
2. Select your site
3. Open **Configuration Editor**
4. Navigate to `system.webServer/aspNetCore/environmentVariables`
5. Add each environment variable

---

## Testing Email Configuration

After setting up, test your email configuration:

### Test Script
Create a file `test_email.py` in your project root:

```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ifla_backend.settings')
django.setup()

from django.core.mail import send_mail

try:
    send_mail(
        'Test Email',
        'This is a test email from IFLA.',
        None,  # Uses DEFAULT_FROM_EMAIL
        ['your-test-email@example.com'],
        fail_silently=False,
    )
    print("✅ Email sent successfully!")
except Exception as e:
    print(f"❌ Error sending email: {e}")
```

Run it:
```bash
python test_email.py
```

---

## Security Best Practices

1. **Never commit passwords to Git**
   - Use `.env` files and add them to `.gitignore`
   - Use environment variables on your server

2. **Use App Passwords (not main password)**
   - For Gmail, always use App Passwords
   - Never use your main account password

3. **Limit Email Access**
   - Use the least privileged access needed
   - Rotate passwords/keys periodically

4. **Monitor Email Sending**
   - Check email service dashboard for delivery issues
   - Set up alerts for failed emails

---

## Troubleshooting

### Gmail: "Username and Password not accepted"
- Make sure you're using an **App Password**, not your regular password
- Ensure 2-Step Verification is enabled
- Try using your full email as username

### "Connection refused" or "Timeout"
- Check firewall settings (port 587 should be open)
- Verify EMAIL_HOST and EMAIL_PORT are correct
- Some hosting providers block SMTP - contact support

### Emails going to Spam
- Verify your domain with SPF and DKIM records
- Use a custom domain email (not @gmail.com for DEFAULT_FROM_EMAIL)
- Warm up your email sending gradually

### "STARTTLS extension not supported"
- Change `EMAIL_USE_TLS=True` to `EMAIL_USE_SSL=True`
- Change port to `465` (for SSL)

---

## Quick Reference: Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `ENVIRONMENT` | Set to `production` for real emails | `production` |
| `EMAIL_HOST` | SMTP server hostname | `smtp.gmail.com` |
| `EMAIL_PORT` | SMTP port (587 for TLS, 465 for SSL) | `587` |
| `EMAIL_USE_TLS` | Use TLS encryption | `True` |
| `EMAIL_USE_SSL` | Use SSL encryption (alternative to TLS) | `False` |
| `EMAIL_HOST_USER` | SMTP username | `your-email@gmail.com` or `apikey` |
| `EMAIL_HOST_PASSWORD` | SMTP password/API key | `your-app-password` |
| `DEFAULT_FROM_EMAIL` | Default sender email address | `noreply@ifla.com` |

---

## Next Steps

1. Choose your email service provider
2. Set up the service and get credentials
3. Set environment variables on your production server
4. Test email sending
5. Monitor email delivery in production

For questions or issues, check your Django logs for detailed error messages.

