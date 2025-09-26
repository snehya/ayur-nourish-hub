#!/usr/bin/env python
"""
Test script for the Enhanced Ayurvedic Diet Generator
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ayurdiet_backend.settings')
django.setup()

from diet_planner.models import Patient
from diet_planner.models import Food
from enhanced_diet_generator import EnhancedAyurvedicDietGenerator, format_diet_plan_output

def test_enhanced_diet_generator():
    print('=== Testing Enhanced Diet Generator ===')
    print(f'Total foods in database: {Food.objects.count()}')
    
    # Create test patient with correct fields
    from users.models import CustomUser
    
    # Get or create a practitioner user
    practitioner, _ = CustomUser.objects.get_or_create(
        username='test_practitioner',
        defaults={'user_type': 'practitioner'}
    )
    
    patient, created = Patient.objects.get_or_create(
        name='Test Patient',
        defaults={
            'practitioner': practitioner,
            'prakriti': 'Vata',
            'vikriti': 'Vata',
            'agni': 'Manda',
            'health_parameters': {'age': 30, 'gender': 'Male', 'conditions': 'None'}
        }
    )
    
    print(f'Patient: {patient.name} ({patient.prakriti}, {patient.vikriti})')
    
    # Generate diet plan
    generator = EnhancedAyurvedicDietGenerator()
    diet_plan = generator.generate_balanced_diet_plan(patient)
    
    # Display results
    print('\n=== DIET PLAN RESULTS ===')
    print(f'Breakfast foods: {len(diet_plan["breakfast"]["foods"])}')
    for food in diet_plan['breakfast']['foods']:
        print(f'  - {food["food"].name}: {food["calories"]} cal, {food["protein"]}g protein')
    
    print(f'\nLunch foods: {len(diet_plan["lunch"]["foods"])}')
    for food in diet_plan['lunch']['foods']:
        print(f'  - {food["food"].name}: {food["calories"]} cal, {food["protein"]}g protein')
    
    print(f'\nDinner foods: {len(diet_plan["dinner"]["foods"])}')
    for food in diet_plan['dinner']['foods']:
        print(f'  - {food["food"].name}: {food["calories"]} cal, {food["protein"]}g protein')
    
    print(f'\nDaily totals: {diet_plan["daily_totals"]["calories"]} cal, {diet_plan["daily_totals"]["protein"]}g protein')
    
    # Count unique foods to check for repetition
    all_food_names = []
    for meal in ['breakfast', 'lunch', 'dinner']:
        for food_item in diet_plan[meal]['foods']:
            all_food_names.append(food_item['food'].name)
    
    unique_foods = len(set(all_food_names))
    total_foods = len(all_food_names)
    print(f'\nFood Variety Analysis:')
    print(f'Total foods across all meals: {total_foods}')
    print(f'Unique foods: {unique_foods}')
    print(f'Food repetition: {total_foods - unique_foods} repeated foods')
    
    # Show Rasa distribution
    print(f'\nRasa Distribution:')
    for rasa, percentage in diet_plan['rasa_analysis'].items():
        if percentage > 0:
            print(f'  {rasa}: {percentage}%')
    
    # Show full formatted output
    print('\n' + '='*80)
    print('FULL FORMATTED DIET PLAN:')
    print('='*80)
    formatted_output = format_diet_plan_output(patient, diet_plan)
    print(formatted_output)

if __name__ == '__main__':
    test_enhanced_diet_generator()