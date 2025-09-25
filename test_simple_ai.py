#!/usr/bin/env python
"""
Simplified AI Integration Test
Tests the endpoint without making actual AI API calls
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(r'C:\Users\sneha\ayurdiet_backend')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ayurdiet_backend.settings')
django.setup()

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import CustomUser
from diet_planner.models import Patient
import json

print("🧪 SIMPLIFIED AI INTEGRATION TEST")
print("=" * 50)

# Get practitioner and patient
practitioner = CustomUser.objects.filter(user_type='practitioner').first()
patient = Patient.objects.first()

if not practitioner or not patient:
    print("❌ Missing test data. Please ensure practitioner and patient exist.")
    exit(1)

print(f"🔐 Using practitioner: {practitioner.username}")
print(f"👥 Testing with patient: {patient.name}")
print(f"📋 Patient details:")
print(f"   • Prakriti: {patient.prakriti}")
print(f"   • Vikriti: {patient.vikriti}")
print(f"   • Agni: {patient.agni}")
print(f"   • Health Parameters: {patient.health_parameters}")

# Generate JWT token
refresh = RefreshToken.for_user(practitioner)
access_token = str(refresh.access_token)

print(f"\n🎫 JWT Token generated: {access_token[:20]}...")

# Test authentication first
client = APIClient()
client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

print("\n🔐 TESTING AUTHENTICATION")
print("-" * 30)

# Test accessing patient list first
patients_response = client.get('/api/patients/')
print(f"📊 Patients endpoint status: {patients_response.status_code}")

if patients_response.status_code == 200:
    print("✅ Authentication successful!")
    patients_data = patients_response.json()
    print(f"📋 Available patients: {len(patients_data)}")
else:
    print(f"❌ Authentication failed: {patients_response.content.decode()}")
    exit(1)

print("\n🧪 TESTING REQUEST FORMAT")
print("-" * 30)

# Test the request format without environment variables
request_body = {'patient_id': patient.id}
print(f"📤 Request body: {json.dumps(request_body, indent=2)}")

# Check environment variables
from decouple import config
try:
    api_url = config('GOOGLE_AI_STUDIO_API_URL')
    api_key = config('GOOGLE_AI_STUDIO_API_KEY')
    print(f"✅ Environment variables loaded")
    print(f"   • API URL: {api_url}")
    print(f"   • API Key: {'*' * (len(api_key) - 8) + api_key[-8:] if len(api_key) > 8 else 'SHORT_KEY'}")
except Exception as e:
    print(f"❌ Environment variable error: {e}")
    exit(1)

print("\n📡 TESTING API ENDPOINT ACCESS")
print("-" * 30)

# Make a simple request to check the endpoint structure
try:
    response = client.post('/api/generate-diet-plan/', request_body, format='json')
    print(f"📊 Response Status: {response.status_code}")
    
    if response.status_code in [200, 201]:
        print("✅ SUCCESS! Endpoint is working")
        response_data = response.json()
        print(f"📄 Response data structure: {list(response_data.keys())}")
    elif response.status_code == 400:
        print("❌ Bad Request")
        print(f"   Response: {response.content.decode()}")
    elif response.status_code == 401:
        print("❌ Unauthorized")
        print(f"   Response: {response.content.decode()}")
    elif response.status_code == 403:
        print("❌ Forbidden")
        print(f"   Response: {response.content.decode()}")
    elif response.status_code == 500:
        print("❌ Server Error")
        # Try to get more details about the error
        error_content = response.content.decode()
        if 'text/html' in response.get('Content-Type', ''):
            print("   HTML error page returned (check Django debug output)")
            # Extract key information from HTML error
            if 'Exception Value:' in error_content:
                lines = error_content.split('\n')
                for i, line in enumerate(lines):
                    if 'Exception Value:' in line and i + 1 < len(lines):
                        print(f"   Exception: {lines[i + 1].strip()}")
                        break
        else:
            print(f"   Response: {error_content}")
    else:
        print(f"❌ Unexpected status: {response.status_code}")
        print(f"   Response: {response.content.decode()}")
        
except Exception as e:
    print(f"❌ Request failed: {e}")

print("\n" + "=" * 50)
print("🧪 SIMPLIFIED TEST COMPLETE!")