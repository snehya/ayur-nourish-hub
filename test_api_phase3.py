#!/usr/bin/env python
import requests
import json

# API Testing Script for Phase 3
print("🚀 Testing Phase 3: Core API Endpoints")
print("=" * 50)

BASE_URL = "http://127.0.0.1:8000"

def test_jwt_authentication():
    """Test JWT authentication with our test user"""
    print("\n🔐 Testing JWT Authentication...")
    
    # Test credentials
    login_data = {
        "username": "testuser",  # Our practitioner test user
        "password": "testpass123"
    }
    
    try:
        response = requests.post(f'{BASE_URL}/api/token/', json=login_data)
        
        if response.status_code == 200:
            tokens = response.json()
            print("✅ JWT Authentication successful!")
            return tokens['access']
        else:
            print(f"❌ Authentication failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error during authentication: {e}")
        return None

def test_foods_api(token=None):
    """Test the Foods API endpoint"""
    print("\n🥘 Testing Foods API...")
    
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
                print(f"   Sample food: {foods[0].get('name', 'Unknown')}")
        else:
            print(f"❌ Foods API failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing Foods API: {e}")

def test_patients_api(token):
    """Test the Patients API endpoint (requires authentication)"""
    print("\n👤 Testing Patients API...")
    
    if not token:
        print("❌ Cannot test Patients API - authentication required")
        return
    
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        # Test GET patients list
        response = requests.get(f'{BASE_URL}/api/patients/', headers=headers)
        print(f"GET /api/patients/ - Status: {response.status_code}")
        
        if response.status_code == 200:
            patients = response.json()
            print(f"✅ Found {len(patients)} patients for practitioner")
            if patients:
                patient = patients[0]
                print(f"   Sample patient: {patient.get('name', 'Unknown')}")
                print(f"   Prakriti: {patient.get('prakriti', 'Not set')}")
        else:
            print(f"❌ Patients API failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing Patients API: {e}")

def test_api_root():
    """Test the API root endpoint"""
    print("\n🏠 Testing API Root...")
    
    try:
        response = requests.get(f'{BASE_URL}/api/')
        print(f"GET /api/ - Status: {response.status_code}")
        
        if response.status_code == 200:
            api_root = response.json()
            print("✅ API Root accessible")
            print("   Available endpoints:")
            for key, url in api_root.items():
                print(f"     {key}: {url}")
        else:
            print(f"❌ API Root failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing API Root: {e}")

def main():
    try:
        # Test API Root first
        test_api_root()
        
        # Test JWT Authentication
        token = test_jwt_authentication()
        
        # Test Foods API (doesn't require authentication for read)
        test_foods_api()
        
        # Test Foods API with authentication
        if token:
            print("\n🔓 Testing Foods API with authentication...")
            test_foods_api(token)
        
        # Test Patients API (requires authentication)
        test_patients_api(token)
        
        print("\n" + "=" * 50)
        print("🎉 Phase 3 API Testing Complete!")
        print("\n📍 You can also test manually by visiting:")
        print("   🌐 http://127.0.0.1:8000/api/ (API Root)")
        print("   🥘 http://127.0.0.1:8000/api/foods/ (Foods API)")
        print("   👤 http://127.0.0.1:8000/api/patients/ (Patients API - requires auth)")
        print("   🔐 http://127.0.0.1:8000/api/token/ (Get JWT Token)")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server.")
        print("   Make sure Django server is running: python manage.py runserver")

if __name__ == "__main__":
    main()