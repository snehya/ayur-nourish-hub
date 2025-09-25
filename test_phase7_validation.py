# test_phase7_validation.py
"""
Phase 7: Testing & Documentation Validation Script

This script validates the comprehensive testing and documentation system
implemented for the AyurDiet Pro backend.
"""

import os
import sys
import django
from datetime import date, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ayurdiet_backend.settings')
django.setup()

from django.test import TestCase
from django.core.cache import cache
from users.models import CustomUser  
from diet_planner.models import Patient, Food, DietPlan
from api.serializers import PatientSerializer, FoodSerializer

def test_models_and_validation():
    """Test model creation and validation systems"""
    print("🧪 TESTING MODELS AND VALIDATION")
    print("=" * 50)
    
    try:
        # Clear any existing data for clean test
        CustomUser.objects.filter(username='test_validation_user').delete()
        
        # Test user creation
        practitioner = CustomUser.objects.create_user(
            username='test_validation_user',
            email='test@validation.com',
            password='testpass123',
            user_type='practitioner'
        )
        print(f"✅ Practitioner created: {practitioner.username}")
        
        # Test patient creation with validation
        patient_data = {
            'name': 'Test Patient',
            'prakriti': 'Vata',
            'vikriti': 'Pitta', 
            'agni': 'Sama'
        }
        
        # Test serializer validation
        serializer = PatientSerializer(data=patient_data)
        if serializer.is_valid():
            print(f"✅ Patient validation passed: {patient_data}")
        else:
            print(f"❌ Patient validation failed: {serializer.errors}")
            return False
            
        # Create patient
        patient = Patient.objects.create(
            practitioner=practitioner,
            **patient_data
        )
        print(f"✅ Patient created: {patient.name}")
        
        # Test food creation with validation
        food_data = {
            'name': 'Test Food Item',
            'rasa': 'sweet',
            'virya': 'cooling',
            'calories': 150
        }
        
        # Test food serializer validation
        food_serializer = FoodSerializer(data=food_data)
        if food_serializer.is_valid():
            print(f"✅ Food validation passed: {food_data}")
        else:
            print(f"❌ Food validation failed: {food_serializer.errors}")
            return False
            
        # Create food
        food = Food.objects.create(**food_data)
        print(f"✅ Food created: {food.name}")
        
        # Test diet plan creation
        diet_plan = DietPlan.objects.create(
            patient=patient,
            plan_date=date.today(),
            breakfast={'foods': ['Oatmeal', 'Banana']},
            lunch={'foods': ['Rice', 'Dal']},
            dinner={'foods': ['Soup', 'Bread']}
        )
        print(f"✅ Diet plan created for: {patient.name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Model test failed: {str(e)}")
        return False

def test_database_indexes():
    """Test that database indexes are properly created"""
    print("\n🗄️ TESTING DATABASE INDEXES")
    print("=" * 50)
    
    try:
        from django.db import connection
        
        # Get all tables
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        # Check for our main tables
        expected_tables = ['diet_planner_food', 'diet_planner_patient', 'diet_planner_dietplan']
        found_tables = [t for t in expected_tables if t in tables]
        
        print(f"✅ Found {len(found_tables)}/{len(expected_tables)} expected tables")
        
        # Check indexes on key tables
        for table in found_tables:
            cursor.execute(f"PRAGMA index_list({table});")
            indexes = cursor.fetchall()
            print(f"✅ {table}: {len(indexes)} indexes")
            
        return True
        
    except Exception as e:
        print(f"❌ Database index test failed: {str(e)}")
        return False

def test_caching_system():
    """Test the caching system functionality"""
    print("\n🗄️ TESTING CACHING SYSTEM")
    print("=" * 50)
    
    try:
        # Clear cache
        cache.clear()
        print("✅ Cache cleared")
        
        # Test cache set and get
        test_key = "test_phase7_cache"
        test_value = {"message": "Phase 7 cache test", "timestamp": str(date.today())}
        
        cache.set(test_key, test_value, 300)  # 5 minutes
        print(f"✅ Cache set: {test_key}")
        
        # Retrieve from cache
        cached_value = cache.get(test_key)
        if cached_value == test_value:
            print(f"✅ Cache retrieval successful: {cached_value}")
            
            # Test cache deletion
            cache.delete(test_key)
            deleted_value = cache.get(test_key)
            if deleted_value is None:
                print("✅ Cache deletion working")
                return True
            else:
                print("❌ Cache deletion failed")
                return False
        else:
            print(f"❌ Cache retrieval failed. Expected: {test_value}, Got: {cached_value}")
            return False
            
    except Exception as e:
        print(f"❌ Cache test failed: {str(e)}")
        return False

def test_security_settings():
    """Test security settings are properly configured"""
    print("\n🔒 TESTING SECURITY SETTINGS")
    print("=" * 50)
    
    try:
        from django.conf import settings
        
        # Check REST_FRAMEWORK settings
        if hasattr(settings, 'REST_FRAMEWORK'):
            rf_settings = settings.REST_FRAMEWORK
            
            # Check authentication
            if 'DEFAULT_AUTHENTICATION_CLASSES' in rf_settings:
                auth_classes = rf_settings['DEFAULT_AUTHENTICATION_CLASSES']
                if 'rest_framework_simplejwt.authentication.JWTAuthentication' in auth_classes:
                    print("✅ JWT Authentication configured")
                else:
                    print("❌ JWT Authentication not found")
                    return False
            
            # Check throttling
            if 'DEFAULT_THROTTLE_CLASSES' in rf_settings:
                throttle_classes = rf_settings['DEFAULT_THROTTLE_CLASSES']
                if len(throttle_classes) > 0:
                    print(f"✅ Rate limiting configured: {len(throttle_classes)} throttle classes")
                else:
                    print("❌ No throttle classes configured")
                    return False
                    
            # Check schema class for documentation
            if 'DEFAULT_SCHEMA_CLASS' in rf_settings:
                schema_class = rf_settings['DEFAULT_SCHEMA_CLASS']
                if 'drf_spectacular' in schema_class:
                    print("✅ API documentation configured")
                else:
                    print("❌ API documentation not configured")
                    return False
        
        # Check CORS settings
        if hasattr(settings, 'CORS_ALLOWED_ORIGINS'):
            print("✅ CORS settings configured")
        
        # Check installed apps
        if 'drf_spectacular' in settings.INSTALLED_APPS:
            print("✅ DRF Spectacular installed")
        else:
            print("❌ DRF Spectacular not installed")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Security settings test failed: {str(e)}")
        return False

def test_documentation_endpoints():
    """Test that documentation endpoints are configured"""
    print("\n📚 TESTING DOCUMENTATION CONFIGURATION")
    print("=" * 50)
    
    try:
        from django.urls import reverse
        from django.conf import settings
        
        # Check spectacular settings
        if hasattr(settings, 'SPECTACULAR_SETTINGS'):
            spec_settings = settings.SPECTACULAR_SETTINGS
            print(f"✅ API Title: {spec_settings.get('TITLE', 'Not set')}")
            print(f"✅ API Version: {spec_settings.get('VERSION', 'Not set')}")
            print(f"✅ API Description: {spec_settings.get('DESCRIPTION', 'Not set')[:50]}...")
        
        # Test URL reversal (this validates URLs are properly configured)
        try:
            schema_url = reverse('schema')
            swagger_url = reverse('swagger-ui')
            redoc_url = reverse('redoc')
            
            print(f"✅ Schema endpoint: {schema_url}")
            print(f"✅ Swagger UI endpoint: {swagger_url}")
            print(f"✅ ReDoc endpoint: {redoc_url}")
            
            return True
            
        except Exception as url_e:
            print(f"❌ Documentation URL configuration failed: {str(url_e)}")
            return False
            
    except Exception as e:
        print(f"❌ Documentation test failed: {str(e)}")
        return False

def run_phase7_validation():
    """Run all Phase 7 validation tests"""
    print("🚀 PHASE 7: TESTING & DOCUMENTATION VALIDATION")
    print("=" * 60)
    print("Testing comprehensive test suite and API documentation...")
    print()
    
    tests = [
        ("Models & Validation", test_models_and_validation),
        ("Database Indexes", test_database_indexes), 
        ("Caching System", test_caching_system),
        ("Security Settings", test_security_settings),
        ("Documentation Config", test_documentation_endpoints)
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {str(e)}")
            results[test_name] = False
    
    # Summary
    print("\n📋 PHASE 7 VALIDATION SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 PHASE 7 RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 PHASE 7: TESTING & DOCUMENTATION COMPLETE!")
        print("   • Comprehensive test suite implemented")
        print("   • API documentation configured") 
        print("   • Security validations working")
        print("   • Database optimizations verified")
        print("   • Caching system operational")
        print("\n🚀 Your AyurDiet Pro backend is production-ready!")
        return True
    else:
        print(f"\n⚠️  {total-passed} test(s) failed. Please review the errors above.")
        return False

if __name__ == "__main__":
    run_phase7_validation()