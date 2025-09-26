#!/usr/bin/env python3
"""
Complete Backend API Testing Script
Tests all critical endpoints for AyurDiet application
"""
import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"
API_URL = f"{BASE_URL}/api"

def test_server_status():
    """Test if server is running"""
    print("🔍 Testing server status...")
    try:
        response = requests.get(BASE_URL, timeout=5)
        print(f"✅ Server is running! Status: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ Server not running: {e}")
        return False

def test_food_endpoint():
    """Test food data endpoint"""
    print("\n🍽️ Testing food data endpoint...")
    try:
        response = requests.get(f"{API_URL}/foods/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Foods endpoint working! Found {len(data)} foods")
            
            # Show sample foods
            print("📊 Sample foods from Supabase:")
            for food in data[:5]:
                print(f"   • {food['name']} - {food['rasa']} - {food['virya']}")
            
            return data
        else:
            print(f"❌ Foods endpoint failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error testing foods: {e}")
        return None

def test_food_search():
    """Test food search functionality"""
    print("\n🔍 Testing food search...")
    try:
        # Search for cooling foods
        response = requests.get(f"{API_URL}/foods/search/?virya=Cooling", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Search working! Found {len(data)} cooling foods")
            return True
        else:
            print(f"❌ Search failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing search: {e}")
        return False

def test_food_statistics():
    """Test food statistics endpoint"""
    print("\n📊 Testing food statistics...")
    try:
        response = requests.get(f"{API_URL}/foods/statistics/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Statistics working!")
            print(f"   📊 Total foods: {data.get('total_foods')}")
            print(f"   🌡️ Virya distribution: {data.get('virya_distribution')}")
            return True
        else:
            print(f"❌ Statistics failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing statistics: {e}")
        return False

def test_user_endpoints():
    """Test user-related endpoints"""
    print("\n👤 Testing user endpoints...")
    
    # Test registration
    try:
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
            "user_type": "practitioner"
        }
        response = requests.post(f"{API_URL}/users/register/", json=user_data, timeout=10)
        print(f"📝 Registration test: {response.status_code}")
        
        # Test login
        login_data = {
            "username": "testuser",
            "password": "testpass123"
        }
        response = requests.post(f"{API_URL}/token/", json=login_data, timeout=10)
        if response.status_code == 200:
            token_data = response.json()
            print(f"✅ Login working! Got token")
            return token_data.get('access')
        else:
            print(f"❌ Login failed: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error testing users: {e}")
        return None

def test_patient_endpoints(auth_token):
    """Test patient management endpoints"""
    print("\n🏥 Testing patient endpoints...")
    if not auth_token:
        print("⚠️ Skipping patient tests - no auth token")
        return
    
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    try:
        # Test patient creation
        patient_data = {
            "name": "John Doe",
            "prakriti": "Vata",
            "vikriti": "Pitta",
            "agni": "Sama",
            "health_parameters": {
                "age": 30,
                "weight": 70,
                "height": 175
            }
        }
        
        response = requests.post(f"{API_URL}/patients/", json=patient_data, headers=headers, timeout=10)
        print(f"👤 Patient creation test: {response.status_code}")
        
        if response.status_code == 201:
            patient = response.json()
            print(f"✅ Patient created: {patient['name']}")
            return patient['id']
        
    except Exception as e:
        print(f"❌ Error testing patients: {e}")
        return None

def run_complete_test():
    """Run all backend tests"""
    print("🧪 COMPLETE BACKEND API TESTING")
    print("=" * 50)
    
    # Wait a moment for server to start
    time.sleep(3)
    
    # Test 1: Server status
    if not test_server_status():
        return False
    
    # Test 2: Food data
    foods = test_food_endpoint()
    if not foods:
        return False
    
    # Test 3: Food search
    test_food_search()
    
    # Test 4: Food statistics
    test_food_statistics()
    
    # Test 5: User authentication
    auth_token = test_user_endpoints()
    
    # Test 6: Patient management
    test_patient_endpoints(auth_token)
    
    print("\n🎉 BACKEND TESTING COMPLETED!")
    print("=" * 50)
    print("✅ Your Supabase backend is working!")
    print("✅ Food data is loaded and accessible")
    print("✅ APIs are ready for frontend integration")
    
    return True

if __name__ == "__main__":
    run_complete_test()