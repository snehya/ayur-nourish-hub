#!/usr/bin/env python
"""
Test the Hybrid AI-Enhanced Diet Generator
Tests both the enhanced nutrition algorithm AND AI integration
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ayurdiet_backend.settings')
django.setup()

from diet_planner.models import Patient, Food
from users.models import CustomUser
from hybrid_ai_diet_generator import HybridAIAyurvedicDietGenerator, format_hybrid_diet_plan_output

def test_hybrid_ai_diet_generator():
    print('🤖🌿 TESTING HYBRID AI-ENHANCED DIET GENERATOR 🌿🤖')
    print('=' * 80)
    print(f'Total foods in database: {Food.objects.count()}')
    
    # Get or create test patient
    practitioner, _ = CustomUser.objects.get_or_create(
        username='test_practitioner',
        defaults={'user_type': 'practitioner'}
    )
    
    patient, created = Patient.objects.get_or_create(
        name='AI Test Patient',
        defaults={
            'practitioner': practitioner,
            'prakriti': 'Vata',
            'vikriti': 'Vata',
            'agni': 'Manda',
            'health_parameters': {'age': 35, 'gender': 'Female', 'conditions': 'Digestive issues'}
        }
    )
    
    print(f'Patient: {patient.name} ({patient.prakriti}, {patient.vikriti}, {patient.agni})')
    
    # Initialize hybrid generator
    generator = HybridAIAyurvedicDietGenerator()
    
    print('\n🤖 AI INTEGRATION TEST:')
    print('-' * 40)
    
    # Test AI recommendations first
    try:
        ai_recommendations = generator.get_ai_enhanced_recommendations(patient)
        print('✅ AI API call successful!')
        print(f'   🎯 Recommended foods: {ai_recommendations.get("recommended_foods", [])[:5]}')
        print(f'   ❌ Foods to avoid: {ai_recommendations.get("avoid_foods", [])[:3]}')
        print(f'   ⏰ Meal timing: {ai_recommendations.get("meal_timing", "Not specified")}')
        ai_working = True
    except Exception as e:
        print(f'⚠️  AI API unavailable (using fallback): {e}')
        ai_working = False
    
    print('\n📊 HYBRID DIET GENERATION:')
    print('-' * 40)
    
    # Generate hybrid diet plan
    diet_plan = generator.generate_hybrid_diet_plan(patient)
    
    # Display results
    print(f'Breakfast foods: {len(diet_plan["breakfast"]["foods"])}')
    for food in diet_plan['breakfast']['foods']:
        ai_flag = '🤖' if food.get('ai_recommended', False) else '  '
        print(f'{ai_flag} - {food["food"].name}: {food["calories"]} cal, {food["protein"]}g protein')
    
    print(f'\nLunch foods: {len(diet_plan["lunch"]["foods"])}')
    for food in diet_plan['lunch']['foods']:
        ai_flag = '🤖' if food.get('ai_recommended', False) else '  '
        print(f'{ai_flag} - {food["food"].name}: {food["calories"]} cal, {food["protein"]}g protein')
    
    print(f'\nDinner foods: {len(diet_plan["dinner"]["foods"])}')
    for food in diet_plan['dinner']['foods']:
        ai_flag = '🤖' if food.get('ai_recommended', False) else '  '
        print(f'{ai_flag} - {food["food"].name}: {food["calories"]} cal, {food["protein"]}g protein')
    
    # Count unique foods and AI recommendations
    all_food_names = []
    ai_recommended_count = 0
    
    for meal in ['breakfast', 'lunch', 'dinner']:
        for food_item in diet_plan[meal]['foods']:
            all_food_names.append(food_item['food'].name)
            if food_item.get('ai_recommended', False):
                ai_recommended_count += 1
    
    unique_foods = len(set(all_food_names))
    total_foods = len(all_food_names)
    
    # Results summary  
    print('\n' + '='*80)
    print('📊 HYBRID SYSTEM PERFORMANCE SUMMARY')
    print('='*80)
    
    print(f'🔢 Total foods: {total_foods}')
    print(f'🎯 Unique foods: {unique_foods}')
    print(f'❌ Food repetition: {total_foods - unique_foods} repeated foods')
    print(f'🤖 AI-recommended foods: {ai_recommended_count}/{total_foods}')
    print(f'📈 Daily calories: {diet_plan["daily_totals"]["calories"]} cal')
    print(f'🥩 Daily protein: {diet_plan["daily_totals"]["protein"]}g')
    
    # Feature comparison
    print(f'\n✅ IMPROVEMENTS ACHIEVED:')
    print(f'   ✅ No food repetition: {unique_foods == total_foods}')
    print(f'   ✅ Adequate nutrition: {diet_plan["daily_totals"]["calories"] >= 1800}')
    print(f'   ✅ Food variety: {unique_foods >= 12}')
    print(f'   ✅ AI personalization: {ai_working and ai_recommended_count > 0}')
    print(f'   ✅ Balanced meals: {all(len(diet_plan[meal]["foods"]) >= 3 for meal in ["breakfast", "lunch", "dinner"])}')
    
    # Rasa distribution
    print(f'\n🎯 Rasa Distribution:')
    for rasa, percentage in diet_plan['rasa_analysis'].items():
        if percentage > 0:
            print(f'   {rasa}: {percentage}%')
    
    # Show formatted output
    print('\n' + '='*80)
    print('📄 FULL FORMATTED DIET PLAN:')
    print('='*80)
    formatted_output = format_hybrid_diet_plan_output(patient, diet_plan)
    print(formatted_output)
    
    return diet_plan

if __name__ == '__main__':
    test_hybrid_ai_diet_generator()