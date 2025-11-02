"""
Quick test script to verify Google OAuth configuration
Run this to check if your Google OAuth credentials are set up correctly:
    python test_google_oauth.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ifla_backend.settings')
django.setup()

from django.conf import settings

def test_google_oauth_config():
    """Test Google OAuth configuration"""
    
    print("=" * 60)
    print("Google OAuth Configuration Test")
    print("=" * 60)
    
    client_id = settings.GOOGLE_OAUTH2_CLIENT_ID
    client_secret = settings.GOOGLE_OAUTH2_CLIENT_SECRET
    redirect_uri = settings.GOOGLE_OAUTH2_REDIRECT_URI
    
    print(f"\n✓ Client ID: {client_id[:50]}..." if client_id else "✗ Client ID: NOT SET")
    print(f"✓ Client Secret: {'*' * (len(client_secret) - 10)}{client_secret[-10:]}" if client_secret else "✗ Client Secret: NOT SET")
    print(f"✓ Redirect URI: {redirect_uri}")
    
    print("\n" + "=" * 60)
    
    if client_id and client_secret:
        print("✅ Google OAuth is configured!")
        print(f"\n📋 Configuration Summary:")
        print(f"   - Client ID: {client_id}")
        print(f"   - Redirect URI: {redirect_uri}")
        print(f"\n🔗 OAuth URL would be:")
        print(f"   https://accounts.google.com/o/oauth2/v2/auth")
        print(f"   ?client_id={client_id[:30]}...")
        print(f"   &redirect_uri={redirect_uri}")
        print(f"\n⚠️  IMPORTANT: Make sure in Google Cloud Console:")
        print(f"   1. Authorized redirect URI matches: {redirect_uri}")
        print(f"   2. Authorized JavaScript origins includes: http://localhost:8000")
        print(f"\n🚀 You can now test Google login at: http://localhost:8000/auth/")
    else:
        print("❌ Google OAuth is NOT fully configured!")
        print("\nPlease set the following environment variables:")
        if not client_id:
            print("   - GOOGLE_OAUTH2_CLIENT_ID")
        if not client_secret:
            print("   - GOOGLE_OAUTH2_CLIENT_SECRET")
        print("\nYou can set them in your .env file or as environment variables.")
    
    print("=" * 60)

if __name__ == '__main__':
    test_google_oauth_config()

