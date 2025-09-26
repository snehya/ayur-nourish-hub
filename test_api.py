import requests
import json

def test_api_endpoints():
    base_url = "http://127.0.0.1:8000/api"
    
    endpoints_to_test = [
        "/foods/",
        "/diet-plan-templates/",
        "/foods/food_categories/",
        "/diet-plan-templates/plan_types/"
    ]
    
    for endpoint in endpoints_to_test:
        try:
            response = requests.get(f"{base_url}{endpoint}")
            print(f"\n🔍 Testing: {endpoint}")
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    print(f"✅ Returned {len(data)} items")
                    if data:
                        print(f"📋 Sample item: {data[0].get('name', 'N/A')}")
                elif isinstance(data, dict):
                    print(f"✅ Returned data: {list(data.keys())}")
            else:
                print(f"❌ Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Connection error for {endpoint}: {str(e)}")
    
    # Test specific food search
    try:
        print(f"\n🔍 Testing: Food search for 'rice'")
        response = requests.get(f"{base_url}/foods/?search=rice")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {len(data)} rice-related foods")
            for food in data:
                print(f"  - {food['name']} (Virya: {food['virya']}, Vata: {food['vata_effect']})")
    except Exception as e:
        print(f"❌ Search test error: {str(e)}")

if __name__ == "__main__":
    test_api_endpoints()