#!/usr/bin/env python
"""
Phase 3 API Testing Script
Tests the Patient Management API and Food Database API endpoints
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def get_jwt_token():
    """Get JWT token for authentication"""
    print("🔐 Getting JWT Token...")
    
    login_data = {
        "username": "testuser",  # Our practitioner test user
        "password": "testpass123"
    }
    
    try:
        response = requests.post(f'{BASE_URL}/api/token/', json=login_data)
        if response.status_code == 200:
            tokens = response.json()
            print("✅ JWT Token obtained successfully!")
            return tokens['access']
        else:
            print(f"❌ Failed to get token: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error getting token: {e}")
        return None

def test_api_root():
    """Test the API root endpoint"""
    print("\n🏠 Testing API Root...")
    try:
        response = requests.get(f'{BASE_URL}/api/')
        print(f"GET /api/ - Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API Root accessible")
            print("📋 Available endpoints:")
            for key, url in data.items():
                print(f"   • {key}: {url}")
            return True
        else:
            print(f"❌ API Root failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_foods_api(token=None):
    """Test the Food Database API"""
    print("\n🥘 Testing Food Database API...")
    
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    try:
        # Test GET foods list
        response = requests.get(f'{BASE_URL}/api/foods/', headers=headers)
        print(f"GET /api/foods/ - Status: {response.status_code}")
        
        if response.status_code == 200:
            foods = response.json()
            print(f"✅ Found {len(foods)} foods in database")
            
            if foods:
                food = foods[0]
                print(f"📋 Sample food data:")
                print(f"   • Name: {food.get('name')}")
                print(f"   • Rasa: {food.get('rasa')}")
                print(f"   • Guna: {food.get('guna')}")
                print(f"   • Virya: {food.get('virya')}")
                print(f"   • Calories: {food.get('calories')}")
                print(f"   • Protein: {food.get('protein')}")
            
            return True
        else:
            print(f"❌ Foods API failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Foods API: {e}")
        return False

def test_patients_api(token):
    """Test the Patient Management API"""
    print("\n👤 Testing Patient Management API...")
    
    if not token:
        print("❌ Cannot test Patients API - JWT token required")
        return False
    
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        # Test GET patients list
        response = requests.get(f'{BASE_URL}/api/patients/', headers=headers)
        print(f"GET /api/patients/ - Status: {response.status_code}")
        
        if response.status_code == 200:
            patients = response.json()
            print(f"✅ Found {len(patients)} patients for current practitioner")
            
            if patients:
                patient = patients[0]
                print(f"📋 Sample patient data:")
                print(f"   • Name: {patient.get('name')}")
                print(f"   • Prakriti: {patient.get('prakriti')}")
                print(f"   • Vikriti: {patient.get('vikriti')}")
                print(f"   • Agni: {patient.get('agni')}")
                print(f"   • Health Parameters: {patient.get('health_parameters')}")
            
            return True
        else:
            print(f"❌ Patients API failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Patients API: {e}")
        return False

def test_unauthorized_patient_access():
    """Test that unauthorized users cannot access patient data"""
    print("\n🔒 Testing Unauthorized Patient Access...")
    
    try:
        # Try to access patients without authentication
        response = requests.get(f'{BASE_URL}/api/patients/')
        print(f"GET /api/patients/ (no auth) - Status: {response.status_code}")
        
        if response.status_code == 401:
            print("✅ Unauthorized access properly blocked")
            return True
        else:
            print(f"❌ Security issue: Unauthorized access allowed")
            return False
            
    except Exception as e:
        print(f"❌ Error testing security: {e}")
        return False

def test_food_permissions(token):
    """Test food API permissions"""
    print("\n🍽️ Testing Food API Permissions...")
    
    # Test without authentication (should allow read)
    try:
        response = requests.get(f'{BASE_URL}/api/foods/')
        if response.status_code == 200:
            print("✅ Anonymous read access to foods working")
        else:
            print("❌ Anonymous read access failed")
    except Exception as e:
        print(f"❌ Error testing anonymous access: {e}")
    
    # Test with authentication
    if token:
        headers = {'Authorization': f'Bearer {token}'}
        try:
            response = requests.get(f'{BASE_URL}/api/foods/', headers=headers)
            if response.status_code == 200:
                print("✅ Authenticated read access to foods working")
            else:
                print("❌ Authenticated read access failed")
        except Exception as e:
            print(f"❌ Error testing authenticated access: {e}")

def main():
    """Main test function"""
    print("🚀 Phase 3 API Testing")
    print("=" * 50)
    
    try:
        # Test API root
        if not test_api_root():
            print("❌ API Root test failed - stopping tests")
            return
        
        # Get JWT token
        token = get_jwt_token()
        
        # Test Foods API
        test_foods_api()
        test_food_permissions(token)
        
        # Test Patients API
        if token:
            test_patients_api(token)
        
        # Test security
        test_unauthorized_patient_access()
        
        print("\n" + "=" * 50)
        print("🎉 Phase 3 API Testing Complete!")
        
        print("\n📍 Manual Testing URLs:")
        print(f"   🌐 API Root: {BASE_URL}/api/")
        print(f"   🥘 Foods API: {BASE_URL}/api/foods/")
        print(f"   👤 Patients API: {BASE_URL}/api/patients/ (requires auth)")
        print(f"   🔐 Get Token: {BASE_URL}/api/token/")
        
        print("\n🔑 Test Credentials:")
        print("   Username: testuser")
        print("   Password: testpass123")
        print("   User Type: practitioner")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server.")
        print("   Make sure Django server is running: python manage.py runserver")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()