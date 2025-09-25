#!/usr/bin/env python
"""
Simple test to verify Django setup and create test user
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ayurdiet_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from diet_planner.models import Patient, Food
from django.db import IntegrityError

User = get_user_model()

def create_test_data():
    """Create test data for integration testing"""
    print("🔧 Setting up test data...")
    
    # Create test user
    try:
        user, created = User.objects.get_or_create(
            username='sneha',
            defaults={
                'email': 'sneha@example.com',
                'is_staff': True,
                'is_superuser': True,
                'user_type': 'practitioner'
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            print(f"✅ Created test user: {user.username}")
        else:
            print(f"✅ Test user exists: {user.username}")
    except Exception as e:
        print(f"❌ Error creating user: {e}")
    
    # Create sample foods if none exist
    if Food.objects.count() == 0:
        sample_foods = [
            {
                'name': 'Rice',
                'rasa': 'Madhura',
                'virya': 'Sheeta',
                'vipaka': 'Madhura',
                'calories': 130,
                'protein': 2.7,
                'carbs': 28,
                'fat': 0.3,
                'fiber': 0.4
            },
            {
                'name': 'Ginger',
                'rasa': 'Katu',
                'virya': 'Ushna',
                'vipaka': 'Madhura',
                'calories': 80,
                'protein': 1.8,
                'carbs': 18,
                'fat': 0.8,
                'fiber': 2
            }
        ]
        
        for food_data in sample_foods:
            try:
                food = Food.objects.create(**food_data)
                print(f"✅ Created sample food: {food.name}")
            except Exception as e:
                print(f"❌ Error creating food: {e}")
    else:
        print(f"✅ {Food.objects.count()} foods already exist")
    
    print("✅ Test data setup complete!")

def test_basic_functionality():
    """Test basic Django functionality"""
    print("\n🧪 Testing basic functionality...")
    
    # Test user authentication
    from django.contrib.auth import authenticate
    user = authenticate(username='sneha', password='password123')
    if user:
        print(f"✅ Authentication working for user: {user.username}")
    else:
        print("❌ Authentication failed")
        return False
    
    # Test model creation
    try:
        patient_count = Patient.objects.count()
        food_count = Food.objects.count()
        print(f"✅ Database accessible - {patient_count} patients, {food_count} foods")
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 AyurDiet Backend Setup Verification")
    print("=" * 50)
    
    create_test_data()
    
    if test_basic_functionality():
        print("\n🎉 Backend setup verification successful!")
        print("✅ Ready for integration testing")
    else:
        print("\n❌ Backend setup issues detected")
        print("Please resolve issues before running integration tests")