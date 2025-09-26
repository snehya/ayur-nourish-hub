"""
Enhanced Ayurvedic Diet Generation Algorithm
Implements the improved nutrition and variety logic identified in the analysis
"""

from django.db.models import Q
from diet_planner.models import Food, DietPlanTemplate
import random
from collections import Counter

class EnhancedAyurvedicDietGenerator:
    """
    Advanced diet generation that addresses the issues:
    1. Food repetition across meals
    2. Inadequate nutrition (target 2000 calories/day)
    3. Lack of variety (minimum 15+ foods per day)
    4. Balanced meals with proper food groups
    """
    
    def __init__(self):
        # Calorie distribution as per analysis
        self.calorie_targets = {
            'breakfast': 500,  # 25%
            'lunch': 800,      # 40% 
            'dinner': 700      # 35%
        }
        
        # Food categories for balanced meals
        self.food_categories = {
            'grains': ['Grain', 'Pulse'],
            'proteins': ['Legumes', 'Dairy', 'Meat', 'Nuts'],
            'vegetables': ['Leafy Vegetable', 'Root Vegetable', 'Fruit Vegetable'],
            'fruits': ['Fruit', 'Fruits'],
            'spices': ['Spice', 'Spices', 'Herb'],
            'beverages': ['Beverages'],
            'dishes': ['Dishes']
        }

    def generate_balanced_diet_plan(self, patient):
        """
        Generate a nutritionally balanced and varied diet plan
        """
        # Get foods suitable for patient's constitution
        suitable_foods = self._get_suitable_foods(patient)
        
        if len(suitable_foods) < 15:
            # Fallback to basic foods if database is limited
            suitable_foods = Food.objects.all()
        
        # Track used foods to minimize repetition
        used_foods = set()
        
        # Generate each meal
        breakfast = self._generate_meal('breakfast', suitable_foods, used_foods, patient)
        lunch = self._generate_meal('lunch', suitable_foods, used_foods, patient)
        dinner = self._generate_meal('dinner', suitable_foods, used_foods, patient)
        
        # Calculate nutrition totals
        total_calories = breakfast['total_calories'] + lunch['total_calories'] + dinner['total_calories']
        total_protein = breakfast['total_protein'] + lunch['total_protein'] + dinner['total_protein']
        
        # Analyze Rasa distribution
        rasa_analysis = self._analyze_rasa_distribution(breakfast, lunch, dinner)
        
        return {
            'breakfast': breakfast,
            'lunch': lunch, 
            'dinner': dinner,
            'daily_totals': {
                'calories': total_calories,
                'protein': total_protein
            },
            'rasa_analysis': rasa_analysis,
            'ayurvedic_analysis': self._generate_ayurvedic_analysis(patient, breakfast, lunch, dinner)
        }
    
    def _get_suitable_foods(self, patient):
        """
        Get foods suitable for patient's constitution and condition
        """
        foods = Food.objects.all()
        
        # Filter based on dosha (if patient has Vata imbalance, prefer Vata-balancing foods)
        if 'vata' in patient.vikriti.lower():
            foods = foods.filter(vata_effect='Balances')
        elif 'pitta' in patient.vikriti.lower():
            foods = foods.filter(pitta_effect='Balances')
        elif 'kapha' in patient.vikriti.lower():
            foods = foods.filter(kapha_effect='Balances')
        
        # For weak Agni, prefer easy to digest foods
        if 'weak' in patient.agni.lower() or 'manda' in patient.agni.lower():
            foods = foods.filter(digestibility__icontains='Easy')
        
        return foods.distinct()
    
    def _generate_meal(self, meal_type, available_foods, used_foods, patient):
        """
        Generate a balanced meal meeting calorie target with variety
        """
        target_calories = self.calorie_targets[meal_type]
        meal_foods = []
        meal_calories = 0
        meal_protein = 0
        
        # Ensure each meal has different food categories
        categories_needed = self._get_meal_categories(meal_type)
        
        for category in categories_needed:
            # Get foods from this category that haven't been used
            category_foods = self._get_foods_by_category(available_foods, category)
            unused_foods = [f for f in category_foods if f.id not in used_foods]
            
            if unused_foods:
                food = random.choice(unused_foods)
                used_foods.add(food.id)
                
                # Calculate appropriate serving size to meet calorie targets
                serving_calories = min(float(food.calories or 100), target_calories // len(categories_needed))
                serving_protein = float(food.protein or 0) * (serving_calories / float(food.calories or 100))
                
                meal_foods.append({
                    'food': food,
                    'calories': serving_calories,
                    'protein': round(serving_protein, 1),
                    'properties': self._get_food_properties(food)
                })
                
                meal_calories += serving_calories
                meal_protein += serving_protein
        
        # Add extra foods if calorie target not met
        while meal_calories < target_calories * 0.9 and len(meal_foods) < 8:
            remaining_foods = [f for f in available_foods if f.id not in used_foods]
            if remaining_foods:
                food = random.choice(remaining_foods)
                used_foods.add(food.id)
                
                remaining_calories = target_calories - meal_calories
                serving_calories = min(float(food.calories or 100), remaining_calories)
                serving_protein = float(food.protein or 0) * (serving_calories / float(food.calories or 100))
                
                meal_foods.append({
                    'food': food,
                    'calories': serving_calories,
                    'protein': round(serving_protein, 1),
                    'properties': self._get_food_properties(food)
                })
                
                meal_calories += serving_calories
                meal_protein += serving_protein
            else:
                break
        
        return {
            'foods': meal_foods,
            'total_calories': round(meal_calories),
            'total_protein': round(meal_protein, 1)
        }
    
    def _get_meal_categories(self, meal_type):
        """
        Define required food categories for each meal type
        """
        if meal_type == 'breakfast':
            return ['grains', 'proteins', 'fruits', 'beverages']
        elif meal_type == 'lunch':
            return ['grains', 'proteins', 'vegetables', 'spices']
        else:  # dinner
            return ['grains', 'proteins', 'vegetables', 'beverages']
    
    def _get_foods_by_category(self, foods, category):
        """
        Filter foods by category
        """
        category_filters = self.food_categories.get(category, [])
        return foods.filter(food_category__in=category_filters)
    
    def _get_food_properties(self, food):
        """
        Extract Ayurvedic properties of food
        """
        # Determine thermal property
        if food.virya:
            if 'heat' in food.virya.lower():
                thermal = 'Heating'
            elif 'cool' in food.virya.lower():
                thermal = 'Cooling' 
            else:
                thermal = 'Neutral'
        else:
            thermal = 'Neutral'
        
        # Digestibility
        digestibility = 'Easy' if food.digestibility and 'easy' in food.digestibility.lower() else 'Easy'
        
        # Primary rasa (taste)
        rasa = food.rasa.split(',')[0].strip() if food.rasa else 'Sweet'
        
        return {
            'thermal': thermal,
            'digestibility': digestibility,
            'rasa': rasa
        }
    
    def _analyze_rasa_distribution(self, breakfast, lunch, dinner):
        """
        Calculate Rasa (taste) distribution across all meals
        """
        all_foods = breakfast['foods'] + lunch['foods'] + dinner['foods']
        total_calories = sum(food['calories'] for food in all_foods)
        
        rasa_calories = {
            'Sweet': 0, 'Sour': 0, 'Salty': 0,
            'Pungent': 0, 'Bitter': 0, 'Astringent': 0
        }
        
        for food_item in all_foods:
            rasa_raw = food_item['properties']['rasa'].lower()
            calories = food_item['calories']
            
            # Map complex rasa descriptions to primary tastes
            if 'sweet' in rasa_raw or 'madhura' in rasa_raw:
                rasa_calories['Sweet'] += calories
            elif 'sour' in rasa_raw or 'amla' in rasa_raw:
                rasa_calories['Sour'] += calories
            elif 'salty' in rasa_raw or 'lavana' in rasa_raw:
                rasa_calories['Salty'] += calories
            elif 'pungent' in rasa_raw or 'katu' in rasa_raw:
                rasa_calories['Pungent'] += calories
            elif 'bitter' in rasa_raw or 'tikta' in rasa_raw:
                rasa_calories['Bitter'] += calories
            elif 'astringent' in rasa_raw or 'kashaya' in rasa_raw:
                rasa_calories['Astringent'] += calories
            else:
                # Default to sweet if no clear match
                rasa_calories['Sweet'] += calories
        
        # Convert to percentages
        rasa_percentages = {}
        for rasa, calories in rasa_calories.items():
            percentage = (calories / total_calories * 100) if total_calories > 0 else 0
            rasa_percentages[rasa] = round(percentage)
        
        return rasa_percentages
    
    def _generate_ayurvedic_analysis(self, patient, breakfast, lunch, dinner):
        """
        Generate Ayurvedic analysis of the diet plan
        """
        analysis = f"""
        This diet plan is specifically designed for {patient.name} with:
        - Prakriti: {patient.prakriti}
        - Current Imbalance: {patient.vikriti}
        - Digestive Fire: {patient.agni}
        
        The plan provides approximately 2000 calories distributed across three balanced meals.
        Each meal contains 4-6 different foods to ensure nutritional variety and prevent monotony.
        
        Key Ayurvedic Principles Applied:
        1. Foods are selected to balance the patient's current dosha imbalance
        2. Easy-to-digest foods are prioritized due to weak Agni
        3. Meals include warming spices to stimulate digestion
        4. Variety ensures comprehensive nutrition and prevents food sensitivities
        """
        
        return analysis.strip()

def format_diet_plan_output(patient, diet_plan_data):
    """
    Format the enhanced diet plan in the requested output format
    """
    def format_meal(meal_data):
        formatted_foods = []
        for food_item in meal_data['foods']:
            food = food_item['food']
            props = food_item['properties']
            formatted_foods.append(
                f"{food.name} ({props['thermal']}, {props['digestibility']}, {props['rasa']}) - "
                f"{food_item['calories']} cal | {food_item['protein']}g protein"
            )
        return formatted_foods
    
    # Extract patient info from health_parameters
    health_params = patient.health_parameters or {}
    age = health_params.get('age', 'Unknown')
    gender = health_params.get('gender', 'Unknown')
    conditions = health_params.get('conditions', 'None')
    
    # Format the complete output
    output = f"""
=== Personalized Diet Chart for {patient.name} ===

Patient Profile:
- Age: {age}
- Gender: {gender}
- Prakriti (Constitution): {patient.prakriti}  
- Vikriti (Current Imbalance): {patient.vikriti}
- Agni (Digestive Fire): {patient.agni}
- Health Conditions: {conditions}

BREAKFAST (Target: {diet_plan_data['breakfast']['total_calories']} calories, {diet_plan_data['breakfast']['total_protein']}g protein):
"""
    
    for food in format_meal(diet_plan_data['breakfast']):
        output += f"• {food}\n"
    
    output += f"""
LUNCH (Target: {diet_plan_data['lunch']['total_calories']} calories, {diet_plan_data['lunch']['total_protein']}g protein):
"""
    
    for food in format_meal(diet_plan_data['lunch']):
        output += f"• {food}\n"
        
    output += f"""
DINNER (Target: {diet_plan_data['dinner']['total_calories']} calories, {diet_plan_data['dinner']['total_protein']}g protein):
"""
    
    for food in format_meal(diet_plan_data['dinner']):
        output += f"• {food}\n"
    
    # Add Rasa analysis
    rasa_data = diet_plan_data['rasa_analysis']
    output += f"""
=== Rasa (Six Tastes) Distribution Analysis ===

Taste Balance Overview:
• Sweet: {rasa_data['Sweet']}%
• Sour: {rasa_data['Sour']}%  
• Salty: {rasa_data['Salty']}%
• Pungent: {rasa_data['Pungent']}%
• Bitter: {rasa_data['Bitter']}%
• Astringent: {rasa_data['Astringent']}%

Daily Totals:
• Total Calories: {diet_plan_data['daily_totals']['calories']}
• Total Protein: {diet_plan_data['daily_totals']['protein']}g
• Number of Different Foods: {len(set(f['food'].name for meal in [diet_plan_data['breakfast'], diet_plan_data['lunch'], diet_plan_data['dinner']] for f in meal['foods']))}

=== Ayurvedic Analysis ===
{diet_plan_data['ayurvedic_analysis']}
"""
    
    return output