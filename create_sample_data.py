#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(r'C:\Users\sneha\ayurdiet_backend')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ayurdiet_backend.settings')
django.setup()

from users.models import CustomUser
from diet_planner.models import Food, Patient, DietPlan
from datetime import date

print("🌟 Creating sample data...")

# Create a practitioner user
practitioner, created = CustomUser.objects.get_or_create(
    username='dr_ayurveda',
    defaults={
        'email': 'doctor@ayurdiet.com',
        'user_type': 'practitioner',
        'first_name': 'Dr. Ayur',
        'last_name': 'Veda'
    }
)
if created:
    practitioner.set_password('practice123')
    practitioner.save()
    print("✅ Created practitioner user")
else:
    print("ℹ️ Practitioner user already exists")

# Create some sample foods
foods_data = [
    {
        'name': 'Basmati Rice',
        'calories': 130.00,
        'protein': 2.70,
        'rasa': 'Sweet',
        'guna': 'Light, Easy to digest',
        'virya': 'Cool'
    },
    {
        'name': 'Turmeric',
        'calories': 29.00,
        'protein': 0.91,
        'rasa': 'Bitter, Pungent',
        'guna': 'Light, Dry',
        'virya': 'Hot'
    },
    {
        'name': 'Ginger',
        'calories': 4.00,
        'protein': 0.09,
        'rasa': 'Pungent',
        'guna': 'Light, Dry',
        'virya': 'Hot'
    }
]

for food_data in foods_data:
    food, created = Food.objects.get_or_create(
        name=food_data['name'],
        defaults=food_data
    )
    if created:
        print(f"✅ Created food: {food.name}")
    else:
        print(f"ℹ️ Food already exists: {food.name}")

# Create a sample patient
patient, created = Patient.objects.get_or_create(
    name='Sample Patient',
    practitioner=practitioner,
    defaults={
        'prakriti': 'Vata',
        'vikriti': 'Pitta',
        'agni': 'Sama',
        'health_parameters': {
            'weight': 70,
            'height': 170,
            'age': 30,
            'allergies': ['nuts'],
            'conditions': ['high_blood_pressure']
        }
    }
)
if created:
    print("✅ Created sample patient")
else:
    print("ℹ️ Sample patient already exists")

# Create a sample diet plan
diet_plan, created = DietPlan.objects.get_or_create(
    patient=patient,
    plan_date=date.today(),
    defaults={
        'breakfast': {
            'foods': ['Basmati Rice', 'Turmeric'],
            'portion': '1 cup rice with pinch of turmeric',
            'time': '8:00 AM'
        },
        'lunch': {
            'foods': ['Basmati Rice', 'Ginger'],
            'portion': '1.5 cups rice with ginger',
            'time': '12:30 PM'
        },
        'dinner': {
            'foods': ['Basmati Rice'],
            'portion': '1 cup rice',
            'time': '7:00 PM'
        },
        'full_plan': {
            'daily_notes': 'Light, easily digestible foods for Vata constitution',
            'recommendations': 'Eat warm foods, avoid cold drinks'
        }
    }
)
if created:
    print("✅ Created sample diet plan")
else:
    print("ℹ️ Sample diet plan already exists")

print(f"\n📊 Current Database Status:")
print(f"   Users: {CustomUser.objects.count()}")
print(f"   Foods: {Food.objects.count()}")
print(f"   Patients: {Patient.objects.count()}")
print(f"   Diet Plans: {DietPlan.objects.count()}")

print("\n🎉 Sample data creation complete!")