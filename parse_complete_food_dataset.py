#!/usr/bin/env python3
"""
Complete Food Item2.txt Parser and Loader
Load ALL 374 foods from the comprehensive Food Item2.txt file
"""
import os
import django
from decimal import Decimal
import csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ayurdiet_backend.settings')
django.setup()

from diet_planner.models import Food

def parse_and_load_complete_dataset():
    print("🌟 LOADING COMPLETE FOOD ITEM2.TXT DATASET (ALL 374 FOODS)")
    print("=" * 70)
    
    file_path = r'c:\Users\sneha\OneDrive\Desktop\Food Item2.txt'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # Split by lines and remove empty lines
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        print(f"📊 File analysis:")
        print(f"   - Total lines: {len(lines)}")
        print(f"   - Header line: 1")
        print(f"   - Data lines: {len(lines) - 1}")
        
        # Skip header line
        data_lines = lines[1:]
        print(f"   - Foods to process: {len(data_lines)}")
        
        added_count = 0
        skipped_count = 0
        error_count = 0
        
        for i, line in enumerate(data_lines):
            try:
                # Split by tab
                parts = line.split('\t')
                
                if len(parts) >= 13:  # Ensure we have all required fields
                    sno = parts[0].strip()
                    name = parts[1].strip()
                    category = parts[2].strip()
                    thermal = parts[3].strip()
                    digestibility = parts[4].strip()
                    rasa = parts[5].strip()
                    calories = float(parts[6].strip()) if parts[6].strip() else 0
                    protein = float(parts[7].strip()) if parts[7].strip() else 0
                    fat = float(parts[8].strip()) if parts[8].strip() else 0
                    carbs = float(parts[9].strip()) if parts[9].strip() else 0
                    vata_effect = parts[10].strip()
                    pitta_effect = parts[11].strip()
                    kapha_effect = parts[12].strip()
                    seasons = parts[13].strip() if len(parts) > 13 else "All seasons"
                    
                    # Check if food already exists
                    if not Food.objects.filter(name=name).exists():
                        Food.objects.create(
                            name=name,
                            food_category=category,
                            calories=Decimal(str(calories)),
                            protein=Decimal(str(protein)),
                            fat=Decimal(str(fat)),
                            carbs=Decimal(str(carbs)),
                            rasa=rasa,
                            virya=thermal,
                            vata_effect=vata_effect,
                            pitta_effect=pitta_effect,
                            kapha_effect=kapha_effect,
                            digestibility=digestibility,
                            seasonal_use=seasons,
                            therapeutic_use=f"SNO {sno} - Complete Food Item2.txt dataset",
                            used_in_plans='Complete 374-food Ayurvedic database'
                        )
                        added_count += 1
                        print(f"✅ Added: {name} ({category})")
                        
                        if added_count % 25 == 0:
                            print(f"   Progress: {added_count}/{len(data_lines)} foods added...")
                            
                    else:
                        skipped_count += 1
                        if skipped_count <= 10:  # Only show first 10 skipped items
                            print(f"⏭️  Skipped: {name} (already exists)")
                        elif skipped_count == 11:
                            print(f"⏭️  ... (hiding additional skipped items)")
                else:
                    error_count += 1
                    print(f"❌ Invalid data format in line {i+2}: {line[:50]}...")
                    
            except Exception as e:
                error_count += 1
                print(f"❌ Error processing line {i+2}: {e}")
    
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return
    
    total_foods = Food.objects.count()
    
    print("\n" + "=" * 70)
    print("🌟 COMPLETE FOOD ITEM2.TXT DATASET LOADING FINISHED!")
    print("=" * 70)
    print(f"✅ New foods added: {added_count}")
    print(f"⏭️  Foods skipped (already exist): {skipped_count}")
    print(f"❌ Errors encountered: {error_count}")
    print(f"📊 Total foods now in database: {total_foods}")
    
    print(f"\n🎯 PROGRESS TOWARD 374-FOOD GOAL:")
    print(f"   📈 Current: {total_foods} foods")
    print(f"   🎯 Target: 374 foods")
    print(f"   📊 Remaining: {max(0, 374 - total_foods)} foods")
    print(f"   💪 Progress: {(total_foods/374)*100:.1f}% complete")
    
    if total_foods >= 374:
        print("\n🎉 MISSION ACCOMPLISHED! Complete 374-food dataset loaded!")
        print("🏆 Your AI diet generator now has the FULL comprehensive food database!")
    elif total_foods >= 300:
        print("\n🌟 EXCELLENT! You have a comprehensive food database!")
    elif total_foods >= 250:
        print("\n🎉 GREAT! You have a substantial food database!")
    else:
        print("\n📈 GOOD PROGRESS! Continue loading more foods for complete coverage.")
    
    print("\n🚀 Enhanced AI diet generation with maximum food variety!")
    
    # Show final category breakdown
    print(f"\n📊 FINAL CATEGORY BREAKDOWN:")
    categories = Food.objects.values_list('food_category', flat=True).distinct()
    for category in sorted(categories):
        count = Food.objects.filter(food_category=category).count()
        print(f"   - {category}: {count} foods")

if __name__ == "__main__":
    parse_and_load_complete_dataset()