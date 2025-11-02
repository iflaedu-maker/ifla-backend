# Google Reviews Setup Guide

Follow these steps to integrate real-time Google reviews into your website.

## Step 1: Get Google Places API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **Places API**:
   - Go to "APIs & Services" > "Library"
   - Search for "Places API"
   - Click "Enable"
4. Create an API Key:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "API Key"
   - Copy your API key

## Step 2: Find Your Google Business Place ID

### Method 1: Using Place ID Finder
1. Go to [Place ID Finder](https://developers.google.com/maps/documentation/javascript/examples/places-placeid-finder)
2. Search for your business
3. Copy the Place ID

### Method 2: Using Your Google Business URL
1. Go to your Google Business Profile
2. Look at the URL - it contains your Place ID
3. Example: `https://www.google.com/maps/place/?q=place_id:ChIJ...`

## Step 3: Configure Your Website

Open `script.js` and find this section:

```javascript
const GOOGLE_CONFIG = {
    apiKey: 'YOUR_GOOGLE_API_KEY', // Replace with your API key
    placeId: 'YOUR_PLACE_ID' // Replace with your Place ID
};
```

Replace the values with your actual API key and Place ID:

```javascript
const GOOGLE_CONFIG = {
    apiKey: 'AIzaSyC...your-actual-key', 
    placeId: 'ChIJ...your-actual-place-id'
};
```

## Step 4: Test Your Integration

1. Save your changes
2. Open your website
3. The reviews section should now display real Google reviews
4. Check the browser console for any errors

## Important Notes

⚠️ **Security**: For production, you should:
- Restrict your API key to specific domains
- Use a backend proxy to hide your API key
- Set up usage limits to prevent abuse

⚠️ **CORS Issues**: Direct browser requests to Google Places API may be blocked by CORS. For production, consider:
- Using a backend server to fetch reviews
- Using Google's official Places API with proper configuration
- Implementing a serverless function (e.g., Vercel, Netlify Functions)

## Alternative: Using a Backend Proxy

For better security, create a backend endpoint:

### Example with Node.js/Express:

```javascript
// server.js
const express = require('express');
const axios = require('axios');
const app = express();

app.get('/api/reviews', async (req, res) => {
    try {
        const response = await axios.get(
            `https://maps.googleapis.com/maps/api/place/details/json`,
            {
                params: {
                    place_id: process.env.PLACE_ID,
                    fields: 'reviews,rating',
                    key: process.env.GOOGLE_API_KEY
                }
            }
        );
        
        // Filter 5-star reviews
        const fiveStarReviews = response.data.result.reviews.filter(
            review => review.rating === 5
        );
        
        res.json({ reviews: fiveStarReviews });
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch reviews' });
    }
});

app.listen(3000);
```

Then update your frontend to call your backend:

```javascript
// In script.js
async function fetchGoogleReviews() {
    try {
        const response = await fetch('/api/reviews');
        const data = await response.json();
        displayReviews(data.reviews);
    } catch (error) {
        console.error('Error:', error);
        displayDemoReviews();
    }
}
```

## Current Behavior

- **With API configured**: Displays real Google reviews (5-star only)
- **Without API configured**: Displays demo reviews automatically
- **If API fails**: Falls back to demo reviews

## Need Help?

If you encounter issues:
1. Check browser console for error messages
2. Verify your API key is correct
3. Ensure Places API is enabled
4. Check API key restrictions
5. Review CORS settings

---

**Note**: The current implementation shows demo reviews. Configure your API credentials to display real reviews from your Google Business Profile.




