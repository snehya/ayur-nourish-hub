#!/usr/bin/env python
"""
Live AI Integration Test
Tests the actual AI API call and diet plan generation
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

print("🧪 LIVE AI INTEGRATION TEST")
print("=" * 50)

# Get practitioner and patient
practitioner = CustomUser.objects.filter(user_type='practitioner').first()
patient = Patient.objects.first()

if not practitioner or not patient:
    print("❌ Missing test data. Please ensure practitioner and patient exist.")
    exit(1)

print(f"🔐 Using practitioner: {practitioner.username}")
print(f"👥 Testing with patient: {patient.name}")

# Generate JWT token
refresh = RefreshToken.for_user(practitioner)
access_token = str(refresh.access_token)

print(f"🎫 JWT Token generated: {access_token[:20]}...")

# Create API client
client = APIClient()
client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

print("\n📡 MAKING API CALL TO GENERATE DIET PLAN")
print("-" * 40)

# Make the API call
response = client.post('/api/generate-diet-plan/', {
    'patient_id': patient.id
}, format='json')

print(f"📊 Response Status: {response.status_code}")
print(f"📄 Response Headers: {dict(response.headers)}")

if response.status_code == 200:
    try:
        response_data = response.json()
        print("\n✅ SUCCESS! Diet plan generated:")
        print("-" * 40)
        print(json.dumps(response_data, indent=2))
        
        # Check if diet plan was saved to database
        from diet_planner.models import DietPlan
        latest_plan = DietPlan.objects.filter(patient=patient).latest('created_at')
        print("\n💾 DATABASE CHECK:")
        print(f"✅ Diet plan saved with ID: {latest_plan.id}")
        print(f"📅 Plan date: {latest_plan.plan_date}")
        print(f"🍽️ Has breakfast data: {'breakfast' in latest_plan.full_plan}")
        print(f"🍽️ Has lunch data: {'lunch' in latest_plan.full_plan}")
        print(f"🍽️ Has dinner data: {'dinner' in latest_plan.full_plan}")
        
    except Exception as e:
        print(f"❌ Error processing response: {e}")
        print(f"Raw response: {response.content}")
        
elif response.status_code == 400:
    print("❌ Bad Request - Check request format")
    print(f"Error details: {response.content.decode()}")
    
elif response.status_code == 401:
    print("❌ Unauthorized - Check JWT token")
    
elif response.status_code == 403:
    print("❌ Forbidden - Check practitioner permissions")
    
elif response.status_code == 500:
    print("❌ Server Error - Check AI API configuration")
    print(f"Error details: {response.content.decode()}")
    
else:
    print(f"❌ Unexpected status code: {response.status_code}")
    print(f"Response: {response.content.decode()}")

print("\n" + "=" * 50)
print("🧪 LIVE TEST COMPLETE!")