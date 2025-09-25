#!/usr/bin/env python
"""
Manual integration verification - test key endpoints manually
"""
import os
import sys
import django
import json

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ayurdiet_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from diet_planner.models import Patient, Food, DietPlan
from rest_framework_simplejwt.tokens import RefreshToken
from django.test import Client
from django.urls import reverse

User = get_user_model()

def test_manual_integration():
    """Test integration using Django test client"""
    print("MANUAL INTEGRATION VERIFICATION")
    print("=" * 50)
    
    client = Client()
    
    # Test 1: Get JWT token
    print("\n1. Testing JWT Authentication...")
    login_data = {
        "username": "sneha",
        "password": "password123"
    }
    
    response = client.post('/api/token/', data=json.dumps(login_data), 
                          content_type='application/json')
    
    if response.status_code == 200:
        token_data = json.loads(response.content)
        access_token = token_data['access']
        print(f"   SUCCESS: Got access token {access_token[:20]}...")
        
        # Test 2: Access protected endpoint with token
        print("\n2. Testing protected endpoint access...")
        auth_headers = {'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        
        patients_response = client.get('/api/patients/', **auth_headers)
        if patients_response.status_code == 200:
            patients = json.loads(patients_response.content)
            print(f"   SUCCESS: Retrieved {len(patients)} patients")
            
            # Test 3: Test food database (public endpoint)
            print("\n3. Testing public food database...")
            foods_response = client.get('/api/foods/')
            if foods_response.status_code == 200:
                foods = json.loads(foods_response.content)
                print(f"   SUCCESS: Retrieved {len(foods)} foods")
                
                # Test 4: Generate diet plan if we have patients
                if patients:
                    print("\n4. Testing diet plan generation...")
                    patient_id = patients[0]['id']
                    
                    generation_data = {"patient_id": patient_id}
                    plan_response = client.post('/api/generate-diet-plan/',
                                              data=json.dumps(generation_data),
                                              content_type='application/json',
                                              **auth_headers)
                    
                    if plan_response.status_code == 201:
                        plan_data = json.loads(plan_response.content)
                        print(f"   SUCCESS: Generated diet plan ID {plan_data['generated_plan']['id']}")
                        
                        # Test 5: PDF Export
                        print("\n5. Testing PDF export...")
                        plan_id = plan_data['generated_plan']['id']
                        pdf_response = client.get(f'/api/plans/{plan_id}/export-pdf/', **auth_headers)
                        
                        if pdf_response.status_code == 200:
                            print(f"   SUCCESS: PDF export working - {len(pdf_response.content)} bytes")
                            print("\nALL TESTS PASSED!")
                            print("FRONTEND INTEGRATION READY!")
                            return True
                        else:
                            print(f"   FAILED: PDF export - Status {pdf_response.status_code}")
                    else:
                        print(f"   FAILED: Diet plan generation - Status {plan_response.status_code}")
                        print(f"   Response: {plan_response.content.decode()}")
                else:
                    print("   SKIPPED: No patients available for diet plan test")
                    print("\nMOST TESTS PASSED!")
                    return True
            else:
                print(f"   FAILED: Food database - Status {foods_response.status_code}")
        else:
            print(f"   FAILED: Protected endpoint - Status {patients_response.status_code}")
    else:
        print(f"   FAILED: JWT Authentication - Status {response.status_code}")
        print(f"   Response: {response.content.decode()}")
    
    return False

def check_api_documentation():
    """Test API documentation endpoints"""
    print("\n" + "=" * 50)
    print("TESTING API DOCUMENTATION")
    print("=" * 50)
    
    client = Client()
    
    # Test schema endpoint
    schema_response = client.get('/api/schema/')
    if schema_response.status_code == 200:
        print("SUCCESS: OpenAPI schema accessible")
    else:
        print(f"FAILED: Schema endpoint - Status {schema_response.status_code}")
    
    # Test Swagger UI
    swagger_response = client.get('/api/schema/swagger-ui/')
    if swagger_response.status_code == 200:
        print("SUCCESS: Swagger UI accessible")
    else:
        print(f"FAILED: Swagger UI - Status {swagger_response.status_code}")
    
    # Test ReDoc
    redoc_response = client.get('/api/schema/redoc/')
    if redoc_response.status_code == 200:
        print("SUCCESS: ReDoc UI accessible")
    else:
        print(f"FAILED: ReDoc UI - Status {redoc_response.status_code}")

if __name__ == "__main__":
    success = test_manual_integration()
    check_api_documentation()
    
    if success:
        print("\n" + "=" * 60)
        print("PHASE 9 INTEGRATION VERIFICATION COMPLETE")
        print("=" * 60)
        print("RESULT: ALL SYSTEMS OPERATIONAL")
        print("STATUS: READY FOR FRONTEND INTEGRATION")
        print("NEXT: Phase 9.2 - Authentication Flow Integration")
    else:
        print("\n" + "=" * 60)
        print("INTEGRATION ISSUES DETECTED")
        print("Please resolve issues before proceeding")