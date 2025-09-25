# simple_integration_test.py
"""
Simple Frontend-Backend Integration Test (no emojis for Windows compatibility)
"""

import requests
import json
from datetime import date, datetime

class SimpleIntegrationTester:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000/api"
        self.token = None
        self.test_patient_id = None
        
    def test_authentication_flow(self):
        """Test the complete authentication flow"""
        print("TESTING AUTHENTICATION FLOW")
        print("=" * 50)
        
        login_data = {
            "username": "sneha",
            "password": "password123"
        }
        
        try:
            response = requests.post(f"{self.base_url}/token/", json=login_data)
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('access')
                print(f"LOGIN SUCCESS - Token: {self.token[:20]}...")
                return True
            else:
                print(f"LOGIN FAILED - Status: {response.status_code}")
                return False
        except Exception as e:
            print(f"AUTHENTICATION ERROR: {str(e)}")
            return False
    
    def test_food_database(self):
        """Test food database access"""
        print("\nTESTING FOOD DATABASE")
        print("=" * 50)
        
        try:
            response = requests.get(f"{self.base_url}/foods/")
            if response.status_code == 200:
                foods = response.json()
                print(f"FOOD DATABASE SUCCESS - {len(foods)} foods found")
                if foods:
                    print(f"Sample food: {foods[0].get('name', 'Unknown')}")
                return True
            else:
                print(f"FOOD DATABASE FAILED - Status: {response.status_code}")
                return False
        except Exception as e:
            print(f"FOOD DATABASE ERROR: {str(e)}")
            return False
    
    def test_patient_management(self):
        """Test patient management"""
        print("\nTESTING PATIENT MANAGEMENT")
        print("=" * 50)
        
        if not self.token:
            print("NO TOKEN AVAILABLE")
            return False
            
        headers = {"Authorization": f"Bearer {self.token}"}
        
        try:
            response = requests.get(f"{self.base_url}/patients/", headers=headers)
            if response.status_code == 200:
                patients = response.json()
                print(f"PATIENT MANAGEMENT SUCCESS - {len(patients)} patients found")
                if patients:
                    self.test_patient_id = patients[0]['id']
                    print(f"Using patient: {patients[0]['name']} (ID: {self.test_patient_id})")
                return True
            else:
                print(f"PATIENT MANAGEMENT FAILED - Status: {response.status_code}")
                return False
        except Exception as e:
            print(f"PATIENT MANAGEMENT ERROR: {str(e)}")
            return False
    
    def test_diet_plan_generation(self):
        """Test diet plan generation"""
        print("\nTESTING DIET PLAN GENERATION")
        print("=" * 50)
        
        if not self.token or not self.test_patient_id:
            print("MISSING TOKEN OR PATIENT ID")
            return False
            
        headers = {"Authorization": f"Bearer {self.token}"}
        generation_data = {"patient_id": self.test_patient_id}
        
        try:
            response = requests.post(f"{self.base_url}/generate-diet-plan/", 
                                   json=generation_data, headers=headers)
            
            if response.status_code == 201:
                plan_data = response.json()
                print("DIET PLAN GENERATION SUCCESS")
                print(f"Plan ID: {plan_data['generated_plan']['id']}")
                return True
            else:
                print(f"DIET PLAN GENERATION FAILED - Status: {response.status_code}")
                print(f"Response: {response.text}")
                return False
        except Exception as e:
            print(f"DIET PLAN GENERATION ERROR: {str(e)}")
            return False
    
    def run_tests(self):
        """Run all tests"""
        print("FRONTEND-BACKEND INTEGRATION TEST SUITE")
        print("=" * 60)
        
        tests = [
            ("Authentication", self.test_authentication_flow),
            ("Food Database", self.test_food_database),
            ("Patient Management", self.test_patient_management),
            ("Diet Plan Generation", self.test_diet_plan_generation),
        ]
        
        results = {}
        for test_name, test_func in tests:
            results[test_name] = test_func()
        
        print("\n" + "=" * 60)
        print("TEST RESULTS SUMMARY")
        print("=" * 60)
        
        passed = 0
        for test_name, result in results.items():
            status = "PASS" if result else "FAIL"
            print(f"{status}: {test_name}")
            if result:
                passed += 1
        
        total = len(results)
        print(f"\nRESULTS: {passed}/{total} tests passed")
        
        if passed == total:
            print("\nSUCCESS: Frontend integration ready!")
            return True
        else:
            print(f"\nFAILED: {total-passed} test(s) failed")
            return False

def main():
    tester = SimpleIntegrationTester()
    return tester.run_tests()

if __name__ == "__main__":
    main()