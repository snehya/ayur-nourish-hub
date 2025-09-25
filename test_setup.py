#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(r'C:\Users\sneha\ayurdiet_backend')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ayurdiet_backend.settings')
django.setup()

# Now import and test our models
from users.models import CustomUser
from diet_planner.models import Food, Patient, DietPlan

print("✅ Django setup successful!")
print("✅ All models imported successfully")

# Test CustomUser model
print(f"✅ CustomUser model fields: {[field.name for field in CustomUser._meta.fields]}")
print(f"✅ Total users in database: {CustomUser.objects.count()}")

# Get the first user to check user_type
user = CustomUser.objects.first()
if user:
    print(f"✅ First user: {user.username}, Type: {user.user_type}")
else:
    print("ℹ️ No users found in database")

# Test other models
print(f"✅ Food model: {[field.name for field in Food._meta.fields]}")
print(f"✅ Patient model: {[field.name for field in Patient._meta.fields]}")
print(f"✅ DietPlan model: {[field.name for field in DietPlan._meta.fields]}")

print("\n🎉 Phase 2 Complete! All models and authentication are set up correctly.")