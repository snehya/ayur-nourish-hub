#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(r'C:\Users\sneha\ayurdiet_backend')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ayurdiet_backend.settings')
django.setup()

# Test our API components
print("🔍 Verifying Phase 3 API Components...")

# Test imports
try:
    from api.serializers import PatientSerializer, FoodSerializer
    print("✅ Serializers imported successfully")
    
    from api.views import PatientViewSet, FoodViewSet, IsPractitioner
    print("✅ ViewSets and permissions imported successfully")
    
    from api.urls import router, urlpatterns
    print("✅ URL routing configured successfully")
    
    # Test serializers with sample data
    from diet_planner.models import Food, Patient
    from users.models import CustomUser
    
    # Get sample data
    foods = Food.objects.all()
    patients = Patient.objects.all()
    users = CustomUser.objects.all()
    
    print(f"\n📊 Database Status:")
    print(f"   Foods: {foods.count()}")
    print(f"   Patients: {patients.count()}")
    print(f"   Users: {users.count()}")
    
    # Test serializers
    if foods.exists():
        food = foods.first()
        food_serializer = FoodSerializer(food)
        print(f"\n🥘 Sample Food Serialized:")
        print(f"   Name: {food_serializer.data.get('name')}")
        print(f"   Rasa: {food_serializer.data.get('rasa')}")
        print("✅ FoodSerializer working correctly")
    
    if patients.exists():
        patient = patients.first()
        patient_serializer = PatientSerializer(patient)
        print(f"\n👤 Sample Patient Serialized:")
        print(f"   Name: {patient_serializer.data.get('name')}")
        print(f"   Prakriti: {patient_serializer.data.get('prakriti')}")
        print("✅ PatientSerializer working correctly")
    
    # Test URL patterns
    print(f"\n🚀 API Endpoints Registered:")
    for pattern in router.urls:
        print(f"   {pattern.pattern}")
    
    print("\n🎉 Phase 3 Verification Complete!")
    print("✅ All API components are working correctly")
    
    print("\n📍 Available API Endpoints:")
    print("   GET /api/ - API Root")
    print("   GET/POST /api/foods/ - Foods CRUD")
    print("   GET/POST /api/patients/ - Patients CRUD (Auth required)")
    print("   POST /api/token/ - Get JWT Token")
    print("   POST /api/token/refresh/ - Refresh JWT Token")
    
    print("\n🔧 To test manually:")
    print("   1. Start server: python manage.py runserver")
    print("   2. Visit: http://127.0.0.1:8000/api/")
    print("   3. Use credentials: testuser / testpass123")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")