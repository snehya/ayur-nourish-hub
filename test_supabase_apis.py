#!/usr/bin/env python3
"""
Test Supabase Food APIs
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_food_apis():
    """Test all food-related API endpoints with Supabase data"""
    print("🧪 Testing Supabase Food APIs...")
    
    # Test 1: Get all foods
    print("\n1️⃣ Testing /api/foods/ (Get all foods)")
    try:
        response = requests.get(f"{BASE_URL}/foods/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Found {len(data)} foods")
            print(f"📊 Sample food: {data[0]['name']} - {data[0]['rasa']} - {data[0]['virya']}")
        else:
            print(f"❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Search by virya (cooling foods)
    print("\n2️⃣ Testing food search by virya=Cooling")
    try:
        response = requests.get(f"{BASE_URL}/foods/search/?virya=Cooling")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Found {len(data)} cooling foods")
            for food in data[:3]:
                print(f"   • {food['name']} - {food['rasa']}")
        else:
            print(f"❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Search by rasa (sweet foods)
    print("\n3️⃣ Testing food search by rasa=Sweet")
    try:
        response = requests.get(f"{BASE_URL}/foods/search/?rasa=Sweet")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Found {len(data)} sweet foods")
            for food in data[:3]:
                print(f"   • {food['name']} - {food['virya']}")
        else:
            print(f"❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: Food statistics
    print("\n4️⃣ Testing food statistics")
    try:
        response = requests.get(f"{BASE_URL}/foods/statistics/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Statistics:")
            print(f"   📊 Total foods: {data['total_foods']}")
            print(f"   🌡️ Virya distribution: {data['virya_distribution']}")
            print(f"   👅 Rasa distribution: {data['rasa_distribution']}")
        else:
            print(f"❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n🎉 Supabase API testing completed!")

if __name__ == "__main__":
    test_food_apis()