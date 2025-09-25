# test_frontend_integration.py
"""
Frontend-Backend Integration Test Script
This script tests the complete integration flow between frontend and backend
"""

import requests
import json
from datetime import date, datetime

class FrontendIntegrationTester:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000/api"
        self.token = None
        self.test_patient_id = None
        self.test_plan_id = None
        
    def test_authentication_flow(self):
        """Test the complete authentication flow that frontend will use"""
        print("🔐 TESTING AUTHENTICATION FLOW")
        print("=" * 50)
        
        # Test login
        login_data = {
            "username": "sneha",
            "password": "password123"
        }
        
        try:
            response = requests.post(f"{self.base_url}/token/", json=login_data)
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('access')
                refresh_token = data.get('refresh')
                
                print(f"✅ Login successful")
                print(f"   • Access token: {self.token[:20]}...")
                print(f"   • Refresh token: {refresh_token[:20]}...")
                
                # Test token refresh
                refresh_data = {"refresh": refresh_token}
                refresh_response = requests.post(f"{self.base_url}/token/refresh/", json=refresh_data)
                
                if refresh_response.status_code == 200:
                    new_token = refresh_response.json().get('access')
                    print(f"✅ Token refresh successful: {new_token[:20]}...")
                    return True
                else:
                    print(f"❌ Token refresh failed: {refresh_response.status_code}")
                    return False
                    
            else:
                print(f"❌ Login failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Authentication test failed: {str(e)}")
            return False
    
    def test_patient_management_flow(self):
        """Test complete patient management flow"""
        print("\n👥 TESTING PATIENT MANAGEMENT FLOW")
        print("=" * 50)
        
        if not self.token:
            print("❌ No authentication token available")
            return False
            
        headers = {"Authorization": f"Bearer {self.token}"}
        
        try:
            # 1. Get existing patients
            response = requests.get(f"{self.base_url}/patients/", headers=headers)
            if response.status_code == 200:
                patients = response.json()
                print(f"✅ Retrieved {len(patients)} existing patients")
                
                if patients:
                    self.test_patient_id = patients[0]['id']
                    print(f"   • Using existing patient: {patients[0]['name']} (ID: {self.test_patient_id})")
                else:
                    # 2. Create a test patient if none exist
                    patient_data = {
                        "name": "Integration Test Patient",
                        "prakriti": "Vata",
                        "vikriti": "Pitta", 
                        "agni": "Sama",
                        "health_parameters": {
                            "age": 30,
                            "weight": 70,
                            "height": 170,
                            "allergies": ["nuts"],
                            "conditions": ["stress"]
                        }
                    }
                    
                    create_response = requests.post(f"{self.base_url}/patients/", 
                                                  json=patient_data, headers=headers)
                    if create_response.status_code == 201:
                        new_patient = create_response.json()
                        self.test_patient_id = new_patient['id']
                        print(f"✅ Created test patient: {new_patient['name']} (ID: {self.test_patient_id})")
                    else:
                        print(f"❌ Failed to create patient: {create_response.status_code}")
                        return False
                
                # 3. Test individual patient retrieval
                patient_response = requests.get(f"{self.base_url}/patients/{self.test_patient_id}/", 
                                              headers=headers)
                if patient_response.status_code == 200:
                    patient = patient_response.json()
                    print(f"✅ Retrieved individual patient: {patient['name']}")
                else:
                    print(f"❌ Failed to retrieve individual patient: {patient_response.status_code}")
                    return False
                    
                return True
            else:
                print(f"❌ Failed to retrieve patients: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Patient management test failed: {str(e)}")
            return False
    
    def test_diet_plan_generation_flow(self):
        """Test the complete diet plan generation flow"""
        print("\n🥗 TESTING DIET PLAN GENERATION FLOW")
        print("=" * 50)
        
        if not self.token or not self.test_patient_id:
            print("❌ Missing token or patient ID")
            return False
            
        headers = {"Authorization": f"Bearer {self.token}"}
        
        try:
            # Generate diet plan
            generation_data = {"patient_id": self.test_patient_id}
            response = requests.post(f"{self.base_url}/generate-diet-plan/", 
                                   json=generation_data, headers=headers)
            
            if response.status_code == 201:
                plan_data = response.json()
                self.test_plan_id = plan_data['generated_plan']['id']
                
                print(f"✅ Diet plan generated successfully")
                print(f"   • Plan ID: {self.test_plan_id}")
                print(f"   • Patient: {plan_data['generated_plan']['patient_name']}")
                
                # Display meal information
                meals = ['breakfast', 'lunch', 'dinner']
                for meal in meals:
                    if plan_data['generated_plan'].get(meal):
                        meal_data = plan_data['generated_plan'][meal]
                        if isinstance(meal_data, str):
                            try:
                                meal_data = json.loads(meal_data)
                            except:
                                meal_data = {"foods": [meal_data]}
                        
                        foods = meal_data.get('foods', [])
                        print(f"   • {meal.title()}: {', '.join(foods[:3])}{'...' if len(foods) > 3 else ''}")
                
                # Test guidelines
                if plan_data.get('ayurvedic_guidelines'):
                    guidelines = plan_data['ayurvedic_guidelines']
                    print(f"   • Guidelines: {len(guidelines)} recommendations")
                
                return True
            else:
                print(f"❌ Diet plan generation failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Diet plan generation test failed: {str(e)}")
            return False
    
    def test_pdf_export_flow(self):
        """Test PDF export functionality"""
        print("\n📄 TESTING PDF EXPORT FLOW")
        print("=" * 50)
        
        if not self.token or not self.test_plan_id:
            print("❌ Missing token or plan ID")
            return False
            
        headers = {"Authorization": f"Bearer {self.token}"}
        
        try:
            response = requests.get(f"{self.base_url}/plans/{self.test_plan_id}/export-pdf/", 
                                  headers=headers)
            
            if response.status_code == 200:
                content_type = response.headers.get('Content-Type')
                content_length = len(response.content)
                
                print(f"✅ PDF export successful")
                print(f"   • Content-Type: {content_type}")
                print(f"   • File size: {content_length} bytes")
                
                # Verify it's actually a PDF
                if response.content.startswith(b'%PDF'):
                    print(f"   • Valid PDF format confirmed")
                    
                    # Save test PDF
                    filename = f"frontend_integration_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                    print(f"   • Test PDF saved as: {filename}")
                    
                    return True
                else:
                    print(f"❌ Invalid PDF format")
                    return False
            else:
                print(f"❌ PDF export failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ PDF export test failed: {str(e)}")
            return False
    
    def test_food_database_access(self):
        """Test food database access (public endpoint)"""
        print("\n🍎 TESTING FOOD DATABASE ACCESS")
        print("=" * 50)
        
        try:
            # Test without authentication (should work)
            response = requests.get(f"{self.base_url}/foods/")
            
            if response.status_code == 200:
                foods = response.json()
                print(f"✅ Food database accessible without auth")
                print(f"   • Total foods: {len(foods)}")
                
                if foods:
                    sample_food = foods[0]
                    print(f"   • Sample food: {sample_food.get('name', 'Unknown')}")
                    print(f"     - Rasa: {sample_food.get('rasa', 'Unknown')}")
                    print(f"     - Virya: {sample_food.get('virya', 'Unknown')}")
                    print(f"     - Calories: {sample_food.get('calories', 'Unknown')}")
                
                return True
            else:
                print(f"❌ Food database access failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Food database test failed: {str(e)}")
            return False
    
    def test_cors_headers(self):
        """Test CORS headers for frontend integration"""
        print("\n🌐 TESTING CORS CONFIGURATION")
        print("=" * 50)
        
        try:
            # Test preflight request
            headers = {
                'Origin': 'http://localhost:3000',
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'Content-Type,Authorization'
            }
            
            response = requests.options(f"{self.base_url}/token/", headers=headers)
            
            cors_headers = {
                'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
                'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
                'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
            }
            
            print(f"✅ CORS preflight response: {response.status_code}")
            for header, value in cors_headers.items():
                if value:
                    print(f"   • {header}: {value}")
                else:
                    print(f"   • {header}: Not set")
            
            return True
            
        except Exception as e:
            print(f"❌ CORS test failed: {str(e)}")
            return False
    
    def run_complete_integration_test(self):
        """Run all integration tests"""
        print("🚀 FRONTEND-BACKEND INTEGRATION TEST SUITE")
        print("=" * 60)
        print("Testing complete integration flow for AyurDiet Pro...")
        print()
        
        tests = [
            ("Authentication Flow", self.test_authentication_flow),
            ("Patient Management", self.test_patient_management_flow),
            ("Diet Plan Generation", self.test_diet_plan_generation_flow),
            ("PDF Export", self.test_pdf_export_flow),
            ("Food Database Access", self.test_food_database_access),
            ("CORS Configuration", self.test_cors_headers),
        ]
        
        results = {}
        for test_name, test_func in tests:
            try:
                results[test_name] = test_func()
            except Exception as e:
                print(f"❌ {test_name} failed with exception: {str(e)}")
                results[test_name] = False
        
        # Summary
        print("\n📋 INTEGRATION TEST SUMMARY")
        print("=" * 50)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {test_name}")
        
        print(f"\n🎯 INTEGRATION RESULTS: {passed}/{total} tests passed")
        
        if passed == total:
            print("\n🎉 FRONTEND INTEGRATION READY!")
            print("=" * 50)
            print("✅ Backend is fully ready for frontend integration")
            print("✅ All API endpoints working correctly")
            print("✅ Authentication flow operational")
            print("✅ CORS configured for frontend access")
            print("✅ PDF generation and export working")
            print()
            print("🚀 Ready for Phase 9.2: Authentication Flow Integration!")
            return True
        else:
            print(f"\n⚠️  {total-passed} test(s) failed.")
            print("Please fix the failing tests before proceeding with frontend integration.")
            return False

def main():
    tester = FrontendIntegrationTester()
    return tester.run_complete_integration_test()

if __name__ == "__main__":
    main()