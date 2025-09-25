"""
Test script for Food Database APIs
Tests all the new endpoints with comprehensive Ayurvedic food data
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_food_apis():
    print("🧪 Testing Food Database APIs")
    print("=" * 50)
    
    # Test 1: Food Statistics API
    print("\n📊 Testing Food Statistics API...")
    try:
        response = requests.get(f"{BASE_URL}/foods/statistics/")
        if response.status_code == 200:
            stats = response.json()
            print("✅ Food Statistics API working!")
            print(f"   📊 Total foods: {stats['overview']['total_foods']}")
            print(f"   🧊 Cooling foods: {stats['ayurvedic_properties']['virya_distribution'].get('Cooling', 0)}")
            print(f"   🔥 Heating foods: {stats['ayurvedic_properties']['virya_distribution'].get('Heating', 0)}")
            print(f"   🍯 Data completeness: {stats['overview']['completion_percentage']}%")
        else:
            print(f"❌ Food Statistics API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Food Statistics API error: {e}")
    
    # Test 2: Food Search API - Search by Virya
    print("\n🔍 Testing Food Search API - Cooling Foods...")
    try:
        response = requests.get(f"{BASE_URL}/foods/search/?virya=Cooling&limit=5")
        if response.status_code == 200:
            data = response.json()
            print("✅ Food Search API (Cooling) working!")
            print(f"   Found {data['count']} cooling foods")
            for food in data['results']:
                print(f"   • {food['name']} - {food['rasa']} - {food['guna']}")
        else:
            print(f"❌ Food Search API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Food Search API error: {e}")
    
    # Test 3: Food Search API - Search by Rasa
    print("\n🍯 Testing Food Search API - Sweet Foods...")
    try:
        response = requests.get(f"{BASE_URL}/foods/search/?rasa=Sweet&limit=5")
        if response.status_code == 200:
            data = response.json()
            print("✅ Food Search API (Sweet) working!")
            print(f"   Found {data['count']} sweet foods")
            for food in data['results']:
                print(f"   • {food['name']} - {food['virya']} - {food['guna']}")
        else:
            print(f"❌ Food Search API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Food Search API error: {e}")
    
    # Test 4: Food Search API - Random Foods
    print("\n🎲 Testing Food Search API - Random Foods...")
    try:
        response = requests.get(f"{BASE_URL}/foods/search/?random=true&limit=3")
        if response.status_code == 200:
            data = response.json()
            print("✅ Food Search API (Random) working!")
            print(f"   Random selection of {len(data['results'])} foods:")
            for food in data['results']:
                print(f"   • {food['name']} - {food['rasa']} - {food['virya']}")
        else:
            print(f"❌ Food Search API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Food Search API error: {e}")
    
    # Test 5: Food Search API - Combined Filters
    print("\n🌿 Testing Food Search API - Light & Cooling Foods...")
    try:
        response = requests.get(f"{BASE_URL}/foods/search/?virya=Cooling&guna=Light&limit=5")
        if response.status_code == 200:
            data = response.json()
            print("✅ Food Search API (Combined Filters) working!")
            print(f"   Found {data['count']} light and cooling foods")
            for food in data['results']:
                print(f"   • {food['name']} - {food['rasa']}")
        else:
            print(f"❌ Food Search API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Food Search API error: {e}")
    
    # Test 6: Standard Food List API
    print("\n📋 Testing Standard Food List API...")
    try:
        response = requests.get(f"{BASE_URL}/foods/?limit=5")
        if response.status_code == 200:
            foods = response.json()
            if isinstance(foods, list):
                print("✅ Food List API working!")
                print(f"   Showing first 5 foods:")
                for food in foods[:5]:
                    print(f"   • {food['name']} - {food.get('virya', 'N/A')}")
            else:
                print(f"✅ Food List API working! (Paginated response)")
        else:
            print(f"❌ Food List API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Food List API error: {e}")
    
    # Test 7: Name Search
    print("\n🔎 Testing Food Search API - Name Search...")
    try:
        response = requests.get(f"{BASE_URL}/foods/search/?search=rice")
        if response.status_code == 200:
            data = response.json()
            print("✅ Food Name Search working!")
            print(f"   Found {data['count']} foods containing 'rice':")
            for food in data['results']:
                print(f"   • {food['name']} - {food['rasa']} - {food['virya']}")
        else:
            print(f"❌ Food Name Search failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Food Name Search error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Food Database API Testing Complete!")
    print("\n🚀 Available Endpoints:")
    print("   📊 Statistics: GET /api/foods/statistics/")
    print("   🔍 Search: GET /api/foods/search/?rasa=Sweet&virya=Cooling")
    print("   📋 List: GET /api/foods/")
    print("   🎲 Random: GET /api/foods/search/?random=true&limit=10")
    print("\n💡 Your AyurDiet food database is ready for diet plan generation!")

if __name__ == '__main__':
    test_food_apis()