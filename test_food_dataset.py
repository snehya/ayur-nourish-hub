#!/usr/bin/env python
"""
Test script to verify food data loading
"""
import os
import sys
import django

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ayurdiet_backend.settings')
django.setup()

from diet_planner.models import Food

def test_food_data():
    print("🧪 Testing Food Dataset Loading")
    print("=" * 50)
    
    # Basic counts
    total_foods = Food.objects.count()
    print(f"📊 Total foods in database: {total_foods}")
    
    # Test Ayurvedic property filtering
    cooling_foods = Food.objects.filter(virya__iexact='Cooling').count()
    heating_foods = Food.objects.filter(virya__iexact='Heating').count()
    print(f"🧊 Cooling foods: {cooling_foods}")
    print(f"🔥 Heating foods: {heating_foods}")
    
    # Test rasa filtering
    sweet_foods = Food.objects.filter(rasa__icontains='Sweet').count()
    bitter_foods = Food.objects.filter(rasa__icontains='Bitter').count()
    pungent_foods = Food.objects.filter(rasa__icontains='Pungent').count()
    print(f"🍯 Sweet rasa foods: {sweet_foods}")
    print(f"🌿 Bitter rasa foods: {bitter_foods}")
    print(f"🌶️  Pungent rasa foods: {pungent_foods}")
    
    # Test guna filtering
    light_foods = Food.objects.filter(guna__icontains='Light').count()
    heavy_foods = Food.objects.filter(guna__icontains='Heavy').count()
    print(f"🪶 Light guna foods: {light_foods}")
    print(f"⚖️  Heavy guna foods: {heavy_foods}")
    
    print("\n🔍 Sample Foods by Category:")
    
    # Sample cooling foods
    print("\n❄️  Cooling Foods (sample):")
    cooling_samples = Food.objects.filter(virya__iexact='Cooling')[:5]
    for food in cooling_samples:
        print(f"   • {food.name} - {food.rasa} - {food.guna}")
    
    # Sample heating foods
    print("\n🔥 Heating Foods (sample):")
    heating_samples = Food.objects.filter(virya__iexact='Heating')[:5]
    for food in heating_samples:
        print(f"   • {food.name} - {food.rasa} - {food.guna}")
    
    # Search functionality test
    print("\n🔍 Search Test - Foods with 'Rice' in name:")
    rice_foods = Food.objects.filter(name__icontains='Rice')
    for food in rice_foods:
        print(f"   • {food.name} - {food.virya} - {food.rasa}")
    
    print("\n✅ Food data loading and filtering tests completed!")
    print(f"🎯 Your database now contains {total_foods} Ayurvedic foods ready for diet planning!")

if __name__ == '__main__':
    test_food_data()