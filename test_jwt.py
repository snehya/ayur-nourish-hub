#!/usr/bin/env python
import requests
import json

# Test JWT Authentication
print("🔐 Testing JWT Authentication...")

# Test data
login_data = {
    "username": "sneha",
    "password": "password123"  # The password we set when creating superuser
}

try:
    # Get JWT token
    response = requests.post('http://127.0.0.1:8000/api/token/', json=login_data)
    
    if response.status_code == 200:
        tokens = response.json()
        print("✅ JWT Token obtained successfully!")
        print(f"   Access Token: {tokens['access'][:50]}...")
        print(f"   Refresh Token: {tokens['refresh'][:50]}...")
        
        # Test token refresh
        refresh_data = {"refresh": tokens['refresh']}
        refresh_response = requests.post('http://127.0.0.1:8000/api/token/refresh/', json=refresh_data)
        
        if refresh_response.status_code == 200:
            new_token = refresh_response.json()
            print("✅ Token refresh successful!")
            print(f"   New Access Token: {new_token['access'][:50]}...")
        else:
            print(f"❌ Token refresh failed: {refresh_response.status_code}")
            print(f"   Response: {refresh_response.text}")
    else:
        print(f"❌ Authentication failed: {response.status_code}")
        print(f"   Response: {response.text}")

except requests.exceptions.ConnectionError:
    print("❌ Could not connect to server. Make sure Django server is running at http://127.0.0.1:8000/")
except Exception as e:
    print(f"❌ Error occurred: {e}")

print("\n🎯 To start the server, run:")
print("   python manage.py runserver")