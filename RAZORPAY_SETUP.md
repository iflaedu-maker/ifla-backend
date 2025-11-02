# Razorpay Payment Gateway Setup Guide

This guide will help you set up Razorpay payment gateway integration for your IFLA enrollment system.

## Step 1: Create Razorpay Account

1. Go to [Razorpay Dashboard](https://dashboard.razorpay.com/)
2. Sign up for a free account
3. Complete the account verification process

## Step 2: Get Your API Keys

1. Log in to your Razorpay Dashboard
2. Go to **Settings** → **API Keys**
3. You'll see two keys:
   - **Key ID** (Public Key) - Safe to expose in frontend
   - **Key Secret** (Private Key) - Keep this SECRET, never expose it

### For Testing:
- Use **Test Mode** keys (shown in the dashboard)
- These keys start with `rzp_test_`

### For Production:
- Activate your account
- Use **Live Mode** keys (start with `rzp_live_`)

## Step 3: Configure Your Settings

### Option 1: Environment Variables (Recommended for Production)

Create a `.env` file in your project root (or use your hosting platform's environment variables):

```bash
RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxxxxx
RAZORPAY_KEY_SECRET=xxxxxxxxxxxxxxxxxxxxx
```

Then update `settings.py` to read from environment:

```python
RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID', '')
RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET', '')
```

### Option 2: Direct Configuration (For Testing Only)

In `ifla_backend/settings.py`, add your keys directly:

```python
RAZORPAY_KEY_ID = 'rzp_test_xxxxxxxxxxxxx'
RAZORPAY_KEY_SECRET = 'xxxxxxxxxxxxxxxxxxxxx'
```

⚠️ **Warning**: Never commit actual keys to version control! Use environment variables in production.

## Step 4: Run Database Migration

After adding the payment fields to the model, run:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Step 5: Set Up Webhook (Optional but Recommended)

Webhooks allow Razorpay to notify your server about payment status updates automatically.

1. In Razorpay Dashboard, go to **Settings** → **Webhooks**
2. Click **Add New Webhook**
3. Enter webhook URL: `https://yourdomain.com/api/courses/payment/webhook/`
4. Select events to listen to:
   - `payment.captured` (Payment successful)
   - `payment.failed` (Payment failed)
5. Save the webhook

The webhook endpoint is already configured at `/api/courses/payment/webhook/`

## Step 6: Test Your Integration

1. Start your Django server: `python manage.py runserver`
2. Complete an enrollment form
3. You'll be redirected to the payment portal
4. Select a payment method and click "Proceed to Pay"
5. You'll see the Razorpay checkout modal
6. Use Razorpay test cards:
   - **Card Number**: `4111 1111 1111 1111`
   - **CVV**: Any 3 digits (e.g., `123`)
   - **Expiry**: Any future date (e.g., `12/25`)
   - **Name**: Any name

## Payment Flow

1. **User submits enrollment form** → Creates `EnrollmentApplication`
2. **Redirects to payment portal** → Shows order summary
3. **User clicks "Proceed to Pay"** → Creates Razorpay order via `/api/courses/payment/create-order/`
4. **Razorpay checkout opens** → User completes payment
5. **Payment success** → Redirects to `/api/courses/payment/success/`
6. **Signature verification** → Updates application status
7. **Redirects to dashboard** → Shows success message

## Payment Methods Supported

- Credit/Debit Cards
- UPI (Google Pay, PhonePe, Paytm, etc.)
- Net Banking
- Wallets (Paytm, Freecharge, etc.)

## Security Features

✅ **Payment Signature Verification**: All payments are verified using Razorpay's signature verification
✅ **CSRF Protection**: All endpoints are protected
✅ **User Authentication**: Only authenticated users can make payments
✅ **Order Validation**: Payment orders are validated before processing

## Troubleshooting

### Payment Gateway Not Configured
- Check if `RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET` are set in settings
- Verify the keys are correct in Razorpay dashboard

### Payment Fails
- Check browser console for JavaScript errors
- Verify network requests in browser DevTools
- Check Django server logs for backend errors

### Signature Verification Fails
- Ensure you're using the correct Key Secret
- Verify the payment data matches exactly
- Check that the order ID matches in Razorpay dashboard

### Webhook Not Working
- Ensure your server is accessible from the internet
- Check webhook URL is correct in Razorpay dashboard
- Verify webhook events are enabled
- Check Django logs for webhook errors

## Production Checklist

- [ ] Switch to Live Mode API keys
- [ ] Set up webhooks for automatic payment updates
- [ ] Use environment variables for keys
- [ ] Enable HTTPS (required for webhooks)
- [ ] Test all payment methods
- [ ] Set up payment success/failure email notifications
- [ ] Monitor payment logs regularly

## Support

- Razorpay Documentation: https://razorpay.com/docs/
- Razorpay Support: support@razorpay.com
- Razorpay Dashboard: https://dashboard.razorpay.com/


