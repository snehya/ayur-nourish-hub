#!/usr/bin/env python3
"""
Manual comprehensive food loader
Load all the missing foods from the comprehensive dataset
"""
import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ayurdiet_backend.settings')
django.setup()

from diet_planner.models import Food

def load_missing_comprehensive_foods():
    print("🌟 LOADING ALL COMPREHENSIVE DATASET FOODS")
    print("=" * 60)
    
    # The full comprehensive foods list from the management command
    comprehensive_foods = [
        # Sweeteners & Natural Options
        {'name': 'Agave Nectar', 'food_category': 'Sweetener', 'virya': 'Cool', 'digestibility': 'Heavy', 'rasa': 'Sweet', 'calories': 310, 'protein': 0.1, 'fat': 0, 'carbs': 76.4, 'vata_effect': 'Balances', 'pitta_effect': 'Slightly increases', 'kapha_effect': 'Increases'},
        {'name': 'Maple Syrup', 'food_category': 'Sweetener', 'virya': 'Warm', 'digestibility': 'Heavy', 'rasa': 'Sweet', 'calories': 260, 'protein': 0, 'fat': 0.1, 'carbs': 67, 'vata_effect': 'Reduces', 'pitta_effect': 'Increases', 'kapha_effect': 'Increases'},
        {'name': 'Raw Honey', 'food_category': 'Sweetener', 'virya': 'Warm', 'digestibility': 'Light', 'rasa': 'Sweet', 'calories': 304, 'protein': 0.3, 'fat': 0, 'carbs': 82.4, 'vata_effect': 'Balances', 'pitta_effect': 'Increases', 'kapha_effect': 'Reduces'},
        
        # Nuts & Seeds  
        {'name': 'Chia Seeds', 'food_category': 'Seeds', 'virya': 'Cool', 'digestibility': 'Heavy', 'rasa': 'Sweet', 'calories': 486, 'protein': 16.5, 'fat': 30.7, 'carbs': 42.1, 'vata_effect': 'Reduces', 'pitta_effect': 'Balances', 'kapha_effect': 'Increases'},
        {'name': 'Hemp Seeds', 'food_category': 'Seeds', 'virya': 'Cool', 'digestibility': 'Heavy', 'rasa': 'Sweet', 'calories': 553, 'protein': 31.6, 'fat': 48.8, 'carbs': 8.7, 'vata_effect': 'Reduces', 'pitta_effect': 'Balances', 'kapha_effect': 'Increases'},
        {'name': 'Pumpkin Seeds', 'food_category': 'Seeds', 'virya': 'Warm', 'digestibility': 'Heavy', 'rasa': 'Sweet', 'calories': 559, 'protein': 30.2, 'fat': 49, 'carbs': 10.7, 'vata_effect': 'Reduces', 'pitta_effect': 'Increases', 'kapha_effect': 'Increases'},
        {'name': 'Sunflower Seeds', 'food_category': 'Seeds', 'virya': 'Warm', 'digestibility': 'Heavy', 'rasa': 'Sweet', 'calories': 584, 'protein': 20.8, 'fat': 51.5, 'carbs': 20, 'vata_effect': 'Reduces', 'pitta_effect': 'Increases', 'kapha_effect': 'Increases'},
        
        # Processed Nut Products
        {'name': 'Almond Butter', 'food_category': 'Processed', 'virya': 'Warm', 'digestibility': 'Heavy', 'rasa': 'Sweet', 'calories': 614, 'protein': 21, 'fat': 56, 'carbs': 19, 'vata_effect': 'Reduces', 'pitta_effect': 'Increases', 'kapha_effect': 'Increases'},
        {'name': 'Cashew Butter', 'food_category': 'Processed', 'virya': 'Warm', 'digestibility': 'Heavy', 'rasa': 'Sweet', 'calories': 587, 'protein': 17.6, 'fat': 49.4, 'carbs': 27.6, 'vata_effect': 'Reduces', 'pitta_effect': 'Increases', 'kapha_effect': 'Increases'},
        
        # Alternative Beverages
        {'name': 'Almond Milk', 'food_category': 'Beverage', 'virya': 'Cool', 'digestibility': 'Light', 'rasa': 'Sweet', 'calories': 17, 'protein': 0.6, 'fat': 1.5, 'carbs': 0.6, 'vata_effect': 'Balances', 'pitta_effect': 'Balances', 'kapha_effect': 'Slightly increases'},
        {'name': 'Coconut Milk', 'food_category': 'Beverage', 'virya': 'Cool', 'digestibility': 'Heavy', 'rasa': 'Sweet', 'calories': 230, 'protein': 2.3, 'fat': 24, 'carbs': 6, 'vata_effect': 'Reduces', 'pitta_effect': 'Balances', 'kapha_effect': 'Increases'},
        {'name': 'Oat Milk', 'food_category': 'Beverage', 'virya': 'Cool', 'digestibility': 'Light', 'rasa': 'Sweet', 'calories': 47, 'protein': 1, 'fat': 1.5, 'carbs': 7.3, 'vata_effect': 'Balances', 'pitta_effect': 'Balances', 'kapha_effect': 'Slightly increases'},
        
        # Tropical & Exotic Fruits
        {'name': 'Dragon Fruit', 'food_category': 'Fruit', 'virya': 'Cool', 'digestibility': 'Light', 'rasa': 'Sweet', 'calories': 60, 'protein': 1.2, 'fat': 0, 'carbs': 13, 'vata_effect': 'Balances', 'pitta_effect': 'Cool', 'kapha_effect': 'Balances'},
        {'name': 'Jackfruit', 'food_category': 'Fruit', 'virya': 'Warm', 'digestibility': 'Heavy', 'rasa': 'Sweet', 'calories': 95, 'protein': 1.7, 'fat': 0.6, 'carbs': 23, 'vata_effect': 'Reduces', 'pitta_effect': 'Increases', 'kapha_effect': 'Increases'},
        {'name': 'Passion Fruit', 'food_category': 'Fruit', 'virya': 'Cool', 'digestibility': 'Light', 'rasa': 'Sweet-Sour', 'calories': 97, 'protein': 2.2, 'fat': 0.7, 'carbs': 23, 'vata_effect': 'Balances', 'pitta_effect': 'Cool', 'kapha_effect': 'Reduces'},
        {'name': 'Rambutan', 'food_category': 'Fruit', 'virya': 'Cool', 'digestibility': 'Light', 'rasa': 'Sweet', 'calories': 82, 'protein': 0.7, 'fat': 0.2, 'carbs': 20.9, 'vata_effect': 'Balances', 'pitta_effect': 'Cool', 'kapha_effect': 'Balances'},
        
        # Alternative Flours
        {'name': 'Quinoa Flour', 'food_category': 'Flour', 'virya': 'Warm', 'digestibility': 'Heavy', 'rasa': 'Sweet', 'calories': 368, 'protein': 13.1, 'fat': 5.8, 'carbs': 69.0, 'vata_effect': 'Reduces', 'pitta_effect': 'Balances', 'kapha_effect': 'Increases'},
        {'name': 'Coconut Flour', 'food_category': 'Flour', 'virya': 'Cool', 'digestibility': 'Heavy', 'rasa': 'Sweet', 'calories': 354, 'protein': 17.6, 'fat': 13.6, 'carbs': 64.0, 'vata_effect': 'Reduces', 'pitta_effect': 'Balances', 'kapha_effect': 'Increases'},
        {'name': 'Almond Flour', 'food_category': 'Flour', 'virya': 'Warm', 'digestibility': 'Heavy', 'rasa': 'Sweet', 'calories': 571, 'protein': 21.2, 'fat': 49.9, 'carbs': 22.3, 'vata_effect': 'Reduces', 'pitta_effect': 'Increases', 'kapha_effect': 'Increases'},
        
        # Specialty Oils
        {'name': 'Almond Oil', 'food_category': 'Oil', 'virya': 'Warm', 'digestibility': 'Heavy', 'rasa': 'Sweet', 'calories': 884, 'protein': 0, 'fat': 100, 'carbs': 0, 'vata_effect': 'Reduces', 'pitta_effect': 'Slightly increases', 'kapha_effect': 'Increases'},
        {'name': 'Avocado Oil', 'food_category': 'Oil', 'virya': 'Cool', 'digestibility': 'Heavy', 'rasa': 'Sweet', 'calories': 884, 'protein': 0, 'fat': 100, 'carbs': 0, 'vata_effect': 'Reduces', 'pitta_effect': 'Balances', 'kapha_effect': 'Increases'},
        
        # Fermented Foods
        {'name': 'Kimchi', 'food_category': 'Fermented Vegetable', 'virya': 'Warm', 'digestibility': 'Light', 'rasa': 'Sour-Pungent', 'calories': 15, 'protein': 1.1, 'fat': 0.5, 'carbs': 2.4, 'vata_effect': 'Reduces', 'pitta_effect': 'Increases', 'kapha_effect': 'Reduces'},
        {'name': 'Sauerkraut', 'food_category': 'Fermented Vegetable', 'virya': 'Cool', 'digestibility': 'Light', 'rasa': 'Sour', 'calories': 19, 'protein': 0.9, 'fat': 0.1, 'carbs': 4.3, 'vata_effect': 'Reduces', 'pitta_effect': 'Slightly increases', 'kapha_effect': 'Reduces'},
        
        # Mushrooms
        {'name': 'Shiitake Mushrooms', 'food_category': 'Vegetable', 'virya': 'Cool', 'digestibility': 'Light', 'rasa': 'Sweet', 'calories': 34, 'protein': 2.2, 'fat': 0.5, 'carbs': 6.8, 'vata_effect': 'Balances', 'pitta_effect': 'Cool', 'kapha_effect': 'Reduces'},
        {'name': 'Oyster Mushrooms', 'food_category': 'Vegetable', 'virya': 'Cool', 'digestibility': 'Light', 'rasa': 'Sweet', 'calories': 33, 'protein': 3.3, 'fat': 0.4, 'carbs': 6.1, 'vata_effect': 'Balances', 'pitta_effect': 'Cool', 'kapha_effect': 'Reduces'},
        
        # Sea Vegetables
        {'name': 'Nori Seaweed', 'food_category': 'Sea Vegetable', 'virya': 'Cool', 'digestibility': 'Light', 'rasa': 'Salty', 'calories': 35, 'protein': 5.8, 'fat': 0.3, 'carbs': 5.1, 'vata_effect': 'Reduces', 'pitta_effect': 'Cool', 'kapha_effect': 'Reduces'},
        {'name': 'Kelp', 'food_category': 'Sea Vegetable', 'virya': 'Cool', 'digestibility': 'Light', 'rasa': 'Salty', 'calories': 43, 'protein': 1.7, 'fat': 0.6, 'carbs': 9.6, 'vata_effect': 'Reduces', 'pitta_effect': 'Cool', 'kapha_effect': 'Reduces'},
        
        # Sprouts & Microgreens
        {'name': 'Broccoli Sprouts', 'food_category': 'Sprouts', 'virya': 'Cool', 'digestibility': 'Light', 'rasa': 'Pungent', 'calories': 20, 'protein': 2.6, 'fat': 0.3, 'carbs': 1.5, 'vata_effect': 'Slightly increases', 'pitta_effect': 'Cool', 'kapha_effect': 'Reduces'},
        {'name': 'Alfalfa Sprouts', 'food_category': 'Sprouts', 'virya': 'Cool', 'digestibility': 'Light', 'rasa': 'Sweet', 'calories': 23, 'protein': 4, 'fat': 0.7, 'carbs': 2.1, 'vata_effect': 'Balances', 'pitta_effect': 'Cool', 'kapha_effect': 'Reduces'},
        
        # Ancient Grains & Pseudocereals
        {'name': 'Amaranth', 'food_category': 'Grain', 'virya': 'Warm', 'digestibility': 'Heavy', 'rasa': 'Sweet', 'calories': 371, 'protein': 13.6, 'fat': 7, 'carbs': 65.2, 'vata_effect': 'Reduces', 'pitta_effect': 'Increases', 'kapha_effect': 'Increases'},
        {'name': 'Teff', 'food_category': 'Grain', 'virya': 'Warm', 'digestibility': 'Heavy', 'rasa': 'Sweet', 'calories': 367, 'protein': 13.3, 'fat': 2.4, 'carbs': 73, 'vata_effect': 'Reduces', 'pitta_effect': 'Slightly increases', 'kapha_effect': 'Increases'},
        {'name': 'Farro', 'food_category': 'Grain', 'virya': 'Warm', 'digestibility': 'Heavy', 'rasa': 'Sweet', 'calories': 340, 'protein': 15, 'fat': 2.5, 'carbs': 67.1, 'vata_effect': 'Reduces', 'pitta_effect': 'Slightly increases', 'kapha_effect': 'Increases'},
        
        # Specialty Beans & Legumes
        {'name': 'Adzuki Beans', 'food_category': 'Legumes', 'virya': 'Cool', 'digestibility': 'Heavy', 'rasa': 'Sweet', 'calories': 329, 'protein': 19.9, 'fat': 0.5, 'carbs': 62.9, 'vata_effect': 'Slightly increases', 'pitta_effect': 'Cool', 'kapha_effect': 'Balances'},
        {'name': 'Black Eyed Peas', 'food_category': 'Legumes', 'virya': 'Cool', 'digestibility': 'Heavy', 'rasa': 'Sweet', 'calories': 336, 'protein': 23.5, 'fat': 1.3, 'carbs': 60.7, 'vata_effect': 'Slightly increases', 'pitta_effect': 'Cool', 'kapha_effect': 'Balances'},
        
        # Unique Vegetables
        {'name': 'Jicama', 'food_category': 'Root Vegetable', 'virya': 'Cool', 'digestibility': 'Light', 'rasa': 'Sweet', 'calories': 38, 'protein': 0.7, 'fat': 0.1, 'carbs': 8.8, 'vata_effect': 'Balances', 'pitta_effect': 'Cool', 'kapha_effect': 'Reduces'},
        {'name': 'Kohlrabi', 'food_category': 'Vegetable', 'virya': 'Cool', 'digestibility': 'Light', 'rasa': 'Sweet', 'calories': 27, 'protein': 1.7, 'fat': 0.1, 'carbs': 6.2, 'vata_effect': 'Slightly increases', 'pitta_effect': 'Cool', 'kapha_effect': 'Reduces'},
        {'name': 'Rutabaga', 'food_category': 'Root Vegetable', 'virya': 'Warm', 'digestibility': 'Heavy', 'rasa': 'Sweet', 'calories': 35, 'protein': 1, 'fat': 0.2, 'carbs': 8.1, 'vata_effect': 'Reduces', 'pitta_effect': 'Slightly increases', 'kapha_effect': 'Balances'},
    ]
    
    added_count = 0
    skipped_count = 0
    
    for food_data in comprehensive_foods:
        # Check if food already exists
        if not Food.objects.filter(name=food_data['name']).exists():
            try:
                Food.objects.create(
                    name=food_data['name'],
                    food_category=food_data['food_category'],
                    calories=Decimal(str(food_data.get('calories', 0))),
                    protein=Decimal(str(food_data.get('protein', 0))),
                    fat=Decimal(str(food_data.get('fat', 0))),
                    carbs=Decimal(str(food_data.get('carbs', 0))),
                    rasa=food_data['rasa'],
                    virya=food_data['virya'],
                    vata_effect=food_data['vata_effect'],
                    pitta_effect=food_data['pitta_effect'],
                    kapha_effect=food_data['kapha_effect'],
                    digestibility=food_data['digestibility'],
                    seasonal_use=food_data.get('seasonal_use', 'All seasons'),
                    therapeutic_use='Comprehensive food dataset',
                    used_in_plans='AI-enhanced diet planning'
                )
                added_count += 1
                print(f"✅ Added: {food_data['name']}")
                
                if added_count % 10 == 0:
                    print(f"   Progress: {added_count} foods added...")
                    
            except Exception as e:
                print(f"❌ Error adding {food_data['name']}: {e}")
        else:
            skipped_count += 1
            print(f"⏭️  Skipped: {food_data['name']} (already exists)")
    
    total_foods = Food.objects.count()
    
    print("\n" + "=" * 60)
    print("🌟 COMPREHENSIVE FOOD LOADING COMPLETE!")
    print("=" * 60)
    print(f"✅ New foods added: {added_count}")
    print(f"⏭️  Foods skipped (already exist): {skipped_count}")
    print(f"📊 Total foods now in database: {total_foods}")
    print("\n🎯 Your database now has the FULL comprehensive food collection!")
    print("🚀 Ready for enhanced AI diet generation with variety!")

if __name__ == "__main__":
    load_missing_comprehensive_foods()