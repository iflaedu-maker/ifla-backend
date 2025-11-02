# EmailJS Setup Guide for IFLA Contact Form

Your contact form is now configured to send emails using EmailJS - a free service that requires no backend!

## Step-by-Step Setup Instructions

### 1. Create an EmailJS Account
1. Go to [https://www.emailjs.com/](https://www.emailjs.com/)
2. Click **Sign Up** (it's FREE!)
3. Sign up with Google, GitHub, or email

### 2. Add an Email Service
1. Once logged in, go to **Email Services** in the dashboard
2. Click **Add New Service**
3. Choose your email provider (Gmail recommended):
   - **Gmail**: Easy setup, just authorize with your Google account
   - **Outlook**: Use your Microsoft account
   - **Other**: You can use any SMTP service
4. Click **Connect Account** and follow the authorization steps
5. Give your service a name (e.g., "IFLA Contact Form")
6. Copy the **Service ID** - you'll need this!

### 3. Create an Email Template
1. Go to **Email Templates** in the dashboard
2. Click **Create New Template**
3. Use this template structure:

**Subject:**
```
New Contact Form Submission from {{from_name}}
```

**Body:**
```
You have received a new message from your IFLA website contact form:

From: {{from_name}}
Email: {{from_email}}
Language Interested In: {{language}}

Message:
{{message}}

---
This email was sent from your IFLA website contact form.
```

4. Click **Save**
5. Copy the **Template ID** - you'll need this!

### 4. Get Your Public Key
1. Go to **Account** → **General** in the dashboard
2. Find your **Public Key** (it looks like: `aBc123XyZ-dEf456GhI`)
3. Copy it - you'll need this!

### 5. Configure Your Website

Open `script.js` and replace these values (around line 201-207):

```javascript
const EMAILJS_CONFIG = {
    serviceID: 'YOUR_SERVICE_ID',      // Replace with Service ID from Step 2
    templateID: 'YOUR_TEMPLATE_ID',    // Replace with Template ID from Step 3
    publicKey: 'YOUR_PUBLIC_KEY'       // Replace with Public Key from Step 4
};
```

**Example:**
```javascript
const EMAILJS_CONFIG = {
    serviceID: 'service_abc1234',
    templateID: 'template_xyz5678',
    publicKey: 'aBc123XyZ-dEf456GhI'
};
```

### 6. Test Your Form!
1. Save the `script.js` file
2. Open your website
3. Fill out the contact form
4. Click Submit
5. Check your email inbox - you should receive the form submission!

## 📧 Where Will Emails Be Sent?

Emails will be sent to the email address you authorized when setting up the Email Service in Step 2.

## 🎯 Customization

### Change Recipient Email
To send emails to a different address:
1. Go to **Email Services** in EmailJS dashboard
2. Edit your service
3. Update the email address

### Customize Email Template
1. Go to **Email Templates**
2. Edit your template
3. Modify the subject and body as needed
4. You can use these variables:
   - `{{from_name}}` - Visitor's name
   - `{{from_email}}` - Visitor's email
   - `{{language}}` - Selected language
   - `{{message}}` - Visitor's message
   - `{{to_name}}` - Your name (set to "IFLA Team" by default)

## 💰 Pricing

EmailJS offers a **FREE tier** with:
- 200 emails per month
- Perfect for most small to medium websites
- No credit card required

If you need more, paid plans start at $7/month for 1000 emails.

## 🔒 Security

- Your email credentials are stored securely on EmailJS servers
- The public key is safe to expose in frontend code
- EmailJS prevents spam by limiting requests per IP

## ⚠️ Current Status

Until you configure EmailJS with your credentials, the form will work in **DEMO MODE**:
- It will show success messages
- No actual emails will be sent
- This lets you test the UI/UX

## 🆘 Need Help?

- EmailJS Documentation: [https://www.emailjs.com/docs/](https://www.emailjs.com/docs/)
- EmailJS Support: Available in their dashboard

---

**That's it! Your contact form will start sending emails to your inbox as soon as you complete these steps. 🎉**

