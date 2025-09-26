"""
Test the patient login functionality
"""
import requests
import json

def test_patient_login():
    print("🧪 TESTING PATIENT LOGIN FUNCTIONALITY")
    print("=" * 50)
    
    # Test 1: Patient Login
    print("\n1. 🔐 Testing Patient Login...")
    login_url = "http://localhost:8000/api/auth/login/"
    login_data = {
        "username": "patient_ravi",
        "password": "demo123",
        "user_type": "patient"
    }
    
    try:
        response = requests.post(login_url, json=login_data)
        if response.status_code == 200:
            login_result = response.json()
            print("   ✅ Patient login successful!")
            print(f"   User: {login_result['user']['username']} ({login_result['user']['user_type']})")
            
            # Get the access token for further requests
            access_token = login_result['tokens']['access']
            
            # Test 2: Patient Dashboard
            print("\n2. 📊 Testing Patient Dashboard...")
            dashboard_url = "http://localhost:8000/api/patient/dashboard/"
            headers = {"Authorization": f"Bearer {access_token}"}
            
            dashboard_response = requests.get(dashboard_url, headers=headers)
            if dashboard_response.status_code == 200:
                dashboard_data = dashboard_response.json()
                print("   ✅ Patient dashboard accessible!")
                print(f"   Patient: {dashboard_data['patient_info']['name']}")
                print(f"   Constitution: {dashboard_data['patient_info']['prakriti']}")
                print(f"   Diet Plans: {len(dashboard_data['diet_plans'])}")
                
                if dashboard_data['diet_plans']:
                    plan = dashboard_data['diet_plans'][0]
                    print(f"   Latest Plan Date: {plan['created_date']}")
                    print(f"   Has Breakfast: {'breakfast' in plan}")
                    print(f"   Has Lunch: {'lunch' in plan}")
                    print(f"   Has Dinner: {'dinner' in plan}")
                
            else:
                print(f"   ❌ Dashboard error: {dashboard_response.status_code}")
                print(f"   Response: {dashboard_response.text}")
            
            # Test 3: Feedback submission
            print("\n3. 💬 Testing Feedback Submission...")
            feedback_url = "http://localhost:8000/api/patient/feedback/"
            feedback_data = {
                "plan_id": 1,
                "meal_type": "breakfast",
                "feedback_type": "followed",
                "notes": "Enjoyed the meal, felt energetic!"
            }
            
            feedback_response = requests.post(feedback_url, json=feedback_data, headers=headers)
            if feedback_response.status_code == 200:
                print("   ✅ Feedback submission successful!")
                feedback_result = feedback_response.json()
                print(f"   Feedback: {feedback_result['feedback']['feedback_type']}")
            else:
                print(f"   ❌ Feedback error: {feedback_response.status_code}")
                print(f"   Response: {feedback_response.text}")
                
        else:
            print(f"   ❌ Login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("   ❌ Server not running! Please start with: python manage.py runserver 8000")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎯 PATIENT LOGIN TEST COMPLETE!")

if __name__ == "__main__":
    test_patient_login()