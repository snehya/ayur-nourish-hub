"""
Hybrid AI-Enhanced Diet Generator
Combines the improved nutritional algorithm with AI personalization
"""

import random
import requests
import json
from decimal import Decimal
from collections import defaultdict
from datetime import date
from decouple import config
from diet_planner.models import Food, DietPlanTemplate


class HybridAIAyurvedicDietGenerator:
    def __init__(self):
        # Daily calorie targets from our enhanced algorithm
        self.daily_calorie_target = 2000
        self.meal_distribution = {
            'breakfast': 0.25,  # 500 calories
            'lunch': 0.40,      # 800 calories  
            'dinner': 0.35      # 700 calories
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

    def get_ai_enhanced_recommendations(self, patient):
        """
        Get AI recommendations for food selection and Ayurvedic insights
        """
        try:
            # Create AI prompt for food recommendations
            prompt = f"""
            As an Ayurvedic nutrition expert, analyze this patient profile and provide food recommendations:
            
            Patient Profile:
            - Prakriti (Constitution): {patient.prakriti}
            - Vikriti (Current Imbalance): {patient.vikriti}
            - Agni (Digestive Fire): {patient.agni}
            - Health Parameters: {patient.health_parameters}
            
            Please provide:
            1. TOP 15 FOODS most suitable for this patient's constitution
            2. FOODS TO AVOID for this specific patient
            3. MEAL TIMING recommendations based on their Agni
            4. AYURVEDIC PRINCIPLES to follow for their constitution
            5. THERAPEUTIC RECOMMENDATIONS for their current imbalance
            
            Format response as JSON with keys: recommended_foods, avoid_foods, meal_timing, ayurvedic_principles, therapeutic_notes
            """
            
            # Prepare AI request
            ai_request_data = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }]
            }
            
            # Make AI API call
            ai_response = requests.post(
                f"{config('GOOGLE_AI_STUDIO_API_URL')}?key={config('GOOGLE_AI_STUDIO_API_KEY')}",
                headers={'Content-Type': 'application/json'},
                json=ai_request_data,
                timeout=30
            )
            
            if ai_response.status_code == 200:
                ai_data = ai_response.json()
                if 'candidates' in ai_data and len(ai_data['candidates']) > 0:
                    ai_content = ai_data['candidates'][0]['content']['parts'][0]['text']
                    
                    # Try to parse as JSON
                    try:
                        ai_recommendations = json.loads(ai_content)
                        return ai_recommendations
                    except json.JSONDecodeError:
                        # If not JSON, extract key information using text processing
                        return self._extract_recommendations_from_text(ai_content)
            
        except Exception as e:
            print(f"AI API call failed: {e}")
        
        # Fallback to basic recommendations if AI fails
        return self._get_fallback_recommendations(patient)
    
    def _extract_recommendations_from_text(self, ai_text):
        """
        Extract recommendations from non-JSON AI response
        """
        return {
            'recommended_foods': ['Basmati Rice', 'Mung Dal', 'Ginger', 'Turmeric', 'Sweet Fruits'],
            'avoid_foods': ['Cold Foods', 'Raw Vegetables', 'Processed Foods'],
            'meal_timing': 'Regular meals at consistent times',
            'ayurvedic_principles': 'Eat warm, cooked foods. Favor sweet, sour, salty tastes.',
            'therapeutic_notes': ai_text[:200] + '...' if len(ai_text) > 200 else ai_text
        }
    
    def _get_fallback_recommendations(self, patient):
        """
        Fallback recommendations if AI is unavailable
        """
        return {
            'recommended_foods': ['Basmati Rice', 'Mung Dal', 'Ginger', 'Ghee', 'Dates'],
            'avoid_foods': ['Cold drinks', 'Raw foods', 'Processed foods'],
            'meal_timing': 'Regular meal times based on Agni strength',
            'ayurvedic_principles': f'Balance {patient.vikriti} dosha through appropriate food choices',
            'therapeutic_notes': 'Focus on warm, easily digestible foods'
        }

    def get_ai_suitable_foods(self, patient, ai_recommendations):
        """
        Filter foods based on both constitution and AI recommendations
        """
        # Start with constitution-based filtering
        suitable_foods = Food.objects.all()
        
        # Filter based on dosha imbalance
        if 'vata' in patient.vikriti.lower():
            suitable_foods = suitable_foods.exclude(vata_effect='Increases')
        elif 'pitta' in patient.vikriti.lower():
            suitable_foods = suitable_foods.exclude(pitta_effect='Increases')
        elif 'kapha' in patient.vikriti.lower():
            suitable_foods = suitable_foods.exclude(kapha_effect='Increases')
        
        # AI-enhanced filtering - prioritize AI recommended foods
        recommended_food_names = ai_recommendations.get('recommended_foods', [])
        if recommended_food_names:
            # Create separate querysets for recommended and other foods
            ai_recommended = suitable_foods.filter(
                name__in=recommended_food_names
            )
            other_suitable = suitable_foods.exclude(
                name__in=recommended_food_names
            )
            
            # Combine with AI recommendations getting priority
            suitable_foods = list(ai_recommended) + list(other_suitable)
        
        return suitable_foods

    def categorize_foods(self, foods):
        """
        Categorize foods into meal components (same as enhanced algorithm)
        """
        categories = {
            'grains': [],
            'proteins': [],
            'vegetables': [],
            'fruits': [],
            'dairy': [],
            'spices': [],
            'beverages': [],
            'others': []
        }
        
        # Convert queryset to list if needed
        if hasattr(foods, 'filter'):
            foods = list(foods)
        
        for food in foods:
            category = food.food_category.lower()
            
            if 'grain' in category or 'cereal' in category:
                categories['grains'].append(food)
            elif 'legume' in category or 'pulse' in category or 'dal' in category:
                categories['proteins'].append(food)
            elif 'vegetable' in category:
                categories['vegetables'].append(food)
            elif 'fruit' in category:
                categories['fruits'].append(food)
            elif 'dairy' in category:
                categories['dairy'].append(food)
            elif 'spice' in category or 'herb' in category:
                categories['spices'].append(food)
            elif 'beverage' in category or 'drink' in category:
                categories['beverages'].append(food)
            else:
                categories['others'].append(food)
        
        return categories

    def create_ai_enhanced_meal(self, meal_type, calorie_target, food_categories, used_foods, ai_recommendations):
        """
        Create meals using both nutritional balance and AI insights
        """
        meal_foods = []
        total_calories = 0
        total_protein = 0
        
        # Meal composition (from enhanced algorithm)
        if meal_type == 'breakfast':
            components = [
                ('grains', 1, 200),
                ('proteins', 1, 150),
                ('fruits', 1, 100),
                ('dairy', 1, 50)
            ]
        elif meal_type == 'lunch':
            components = [
                ('grains', 1, 250),
                ('proteins', 1, 300),
                ('vegetables', 2, 100),
                ('others', 1, 150)
            ]
        else:  # dinner
            components = [
                ('grains', 1, 200),
                ('proteins', 1, 300),
                ('vegetables', 1, 100),
                ('beverages', 1, 100)
            ]
        
        # Get AI recommended foods for prioritization
        ai_recommended_names = ai_recommendations.get('recommended_foods', [])
        
        # Select foods for each component
        for category, count, target_cal in components:
            if category in food_categories and food_categories[category]:
                available = [f for f in food_categories[category] if f.id not in used_foods]
                
                if available:
                    # Prioritize AI recommended foods
                    ai_priority = [f for f in available if f.name in ai_recommended_names]
                    other_foods = [f for f in available if f.name not in ai_recommended_names]
                    
                    # Select from AI recommended first, then others
                    selection_pool = ai_priority + other_foods
                    selected = selection_pool[:count] if len(selection_pool) >= count else selection_pool
                    
                    for food in selected:
                        calories = float(food.calories or 100)
                        protein = float(food.protein or 3)
                        
                        # Adjust portion to meet target calories (more generous portions)
                        portion_multiplier = min(target_cal / calories, 3.0) if calories > 0 else 1.5
                        adjusted_calories = calories * portion_multiplier
                        adjusted_protein = protein * portion_multiplier
                        
                        # AI-enhanced properties description
                        thermal = 'Heating' if 'heat' in (food.virya or '').lower() else 'Cooling' if 'cool' in (food.virya or '').lower() else 'Neutral'
                        properties = f"({thermal}, {food.digestibility or 'Easy'}, {food.rasa or 'Sweet'})"
                        
                        meal_foods.append({
                            'food': food,
                            'calories': round(adjusted_calories),
                            'protein': round(adjusted_protein, 1),
                            'properties': properties,
                            'ai_recommended': food.name in ai_recommended_names
                        })
                        
                        total_calories += adjusted_calories
                        total_protein += adjusted_protein
                        used_foods.add(food.id)
        
        # Add extra foods if calorie target not met
        all_available_foods = []
        for category_foods in food_categories.values():
            all_available_foods.extend(category_foods)
        
        while total_calories < calorie_target * 0.85 and len(meal_foods) < 8:
            remaining_foods = [f for f in all_available_foods if f.id not in used_foods]
            if remaining_foods:
                # Prioritize AI recommended foods for extra additions
                ai_priority = [f for f in remaining_foods if f.name in ai_recommended_names]
                selection_pool = ai_priority if ai_priority else remaining_foods
                
                food = selection_pool[0]  # Take first available
                used_foods.add(food.id)
                
                calories = float(food.calories or 100)
                protein = float(food.protein or 3)
                
                remaining_target = calorie_target - total_calories
                portion_multiplier = min(remaining_target / calories, 2.0) if calories > 0 else 1.0
                adjusted_calories = calories * portion_multiplier
                adjusted_protein = protein * portion_multiplier
                
                thermal = 'Heating' if 'heat' in (food.virya or '').lower() else 'Cooling' if 'cool' in (food.virya or '').lower() else 'Neutral'
                properties = f"({thermal}, {food.digestibility or 'Easy'}, {food.rasa or 'Sweet'})"
                
                meal_foods.append({
                    'food': food,
                    'calories': round(adjusted_calories),
                    'protein': round(adjusted_protein, 1),
                    'properties': properties,
                    'ai_recommended': food.name in ai_recommended_names
                })
                
                total_calories += adjusted_calories
                total_protein += adjusted_protein
            else:
                break
        
        return {
            'foods': meal_foods,
            'total_calories': round(total_calories),
            'total_protein': round(total_protein, 1)
        }

    def calculate_rasa_distribution(self, all_meals):
        """
        Calculate rasa distribution (same as enhanced algorithm)
        """
        rasa_calories = defaultdict(int)
        total_calories = 0
        
        for meal in all_meals.values():
            for food_item in meal['foods']:
                rasa_raw = (food_item['food'].rasa or 'sweet').lower()
                calories = food_item['calories']
                
                # Map to primary tastes
                if 'sweet' in rasa_raw:
                    rasa_calories['Sweet'] += calories
                elif 'sour' in rasa_raw:
                    rasa_calories['Sour'] += calories
                elif 'salty' in rasa_raw:
                    rasa_calories['Salty'] += calories
                elif 'pungent' in rasa_raw:
                    rasa_calories['Pungent'] += calories
                elif 'bitter' in rasa_raw:
                    rasa_calories['Bitter'] += calories
                elif 'astringent' in rasa_raw:
                    rasa_calories['Astringent'] += calories
                else:
                    rasa_calories['Sweet'] += calories
                
                total_calories += calories
        
        # Calculate percentages
        rasa_distribution = {}
        for rasa in ['Sweet', 'Sour', 'Salty', 'Pungent', 'Bitter', 'Astringent']:
            percentage = (rasa_calories[rasa] / total_calories * 100) if total_calories > 0 else 0
            rasa_distribution[rasa] = round(percentage)
        
        return rasa_distribution

    def generate_ai_enhanced_analysis(self, patient, rasa_distribution, daily_totals, ai_recommendations):
        """
        Generate comprehensive analysis combining nutrition and AI insights
        """
        analysis = []
        
        # Basic constitution analysis
        analysis.append(f"Diet plan customized for {patient.prakriti} constitution with {patient.vikriti} imbalance")
        
        # AI insights
        ai_principles = ai_recommendations.get('ayurvedic_principles', '')
        if ai_principles:
            analysis.append(f"AI Recommendation: {ai_principles}")
        
        # Nutritional analysis
        if daily_totals['calories'] >= 1800:
            analysis.append("✅ Nutritionally adequate caloric intake achieved")
        if daily_totals['protein'] >= 50:
            analysis.append("✅ Sufficient protein for daily requirements")
        
        # Therapeutic notes from AI
        therapeutic = ai_recommendations.get('therapeutic_notes', '')
        if therapeutic:
            analysis.append(f"Therapeutic Focus: {therapeutic}")
        
        # Meal timing from AI
        timing = ai_recommendations.get('meal_timing', '')
        if timing:
            analysis.append(f"Optimal Timing: {timing}")
        
        return analysis

    def generate_hybrid_diet_plan(self, patient):
        """
        Main method combining enhanced nutrition algorithm with AI personalization
        """
        # Step 1: Get AI recommendations
        print("🤖 Getting AI recommendations...")
        ai_recommendations = self.get_ai_enhanced_recommendations(patient)
        
        # Step 2: Get suitable foods with AI enhancement
        suitable_foods = self.get_ai_suitable_foods(patient, ai_recommendations)
        
        # Step 3: Categorize foods for balanced meal creation
        food_categories = self.categorize_foods(suitable_foods)
        
        # Step 4: Track used foods to avoid repetition
        used_foods = set()
        
        # Step 5: Generate AI-enhanced meals
        meals = {}
        for meal_type, distribution in self.meal_distribution.items():
            calorie_target = self.daily_calorie_target * distribution
            meals[meal_type] = self.create_ai_enhanced_meal(
                meal_type, calorie_target, food_categories, used_foods, ai_recommendations
            )
        
        # Step 6: Calculate daily totals
        daily_calories = sum(meal['total_calories'] for meal in meals.values())
        daily_protein = sum(meal['total_protein'] for meal in meals.values())
        
        daily_totals = {
            'calories': daily_calories,
            'protein': round(daily_protein, 1),
            'meals': len(meals)
        }
        
        # Step 7: Calculate rasa distribution
        rasa_distribution = self.calculate_rasa_distribution(meals)
        
        # Step 8: Generate comprehensive analysis
        ayurvedic_analysis = self.generate_ai_enhanced_analysis(
            patient, rasa_distribution, daily_totals, ai_recommendations
        )
        
        return {
            'breakfast': meals['breakfast'],
            'lunch': meals['lunch'],
            'dinner': meals['dinner'],
            'daily_totals': daily_totals,
            'rasa_analysis': rasa_distribution,
            'ayurvedic_analysis': ayurvedic_analysis,
            'ai_recommendations': ai_recommendations  # Include AI insights
        }


def format_hybrid_diet_plan_output(patient, diet_plan_data):
    """
    Format the hybrid AI-enhanced diet plan
    """
    # Extract patient info
    health_params = patient.health_parameters or {}
    age = health_params.get('age', 'Unknown')
    gender = health_params.get('gender', 'Unknown')
    conditions = health_params.get('conditions', 'None')
    
    output = []
    
    # Header
    output.append("=" * 80)
    output.append("🤖🌿 AI-ENHANCED AYURVEDIC DIET PLAN 🌿🤖")
    output.append("=" * 80)
    
    # Patient details
    output.append(f"\n👤 Patient: {patient.name}")
    output.append(f"📊 Age: {age} | Gender: {gender}")
    output.append(f"🔬 Prakriti: {patient.prakriti} | Agni: {patient.agni}")
    output.append(f"⚖️  Current Imbalance: {patient.vikriti}")
    output.append(f"🏥 Health Conditions: {conditions}")
    
    # AI Recommendations Section
    ai_rec = diet_plan_data.get('ai_recommendations', {})
    output.append(f"\n🤖 AI PERSONALIZATION INSIGHTS:")
    output.append(f"   🎯 Recommended Foods: {', '.join(ai_rec.get('recommended_foods', [])[:5])}")
    output.append(f"   ❌ Foods to Avoid: {', '.join(ai_rec.get('avoid_foods', [])[:3])}")
    output.append(f"   ⏰ Meal Timing: {ai_rec.get('meal_timing', 'Regular intervals')}")
    
    # Diet plan
    output.append(f"\n🍽️ PERSONALIZED DIET CHART")
    output.append("-" * 60)
    
    # Meals with AI recommendations marked
    meal_names = {'breakfast': '🌅 Breakfast', 'lunch': '☀️ Lunch', 'dinner': '🌙 Dinner'}
    
    for meal_type in ['breakfast', 'lunch', 'dinner']:
        meal_data = diet_plan_data[meal_type]
        output.append(f"\n{meal_names[meal_type]}:")
        
        for food_item in meal_data['foods']:
            food_name = food_item['food'].name
            properties = food_item['properties']
            calories = food_item['calories']
            protein = food_item['protein']
            ai_flag = "🤖" if food_item.get('ai_recommended', False) else "  "
            
            output.append(f"{ai_flag}• {food_name} {properties} - {calories} cal | {protein}g protein")
        
        output.append(f"   Total: {meal_data['total_calories']} calories | {meal_data['total_protein']}g protein")
    
    # Daily totals
    output.append(f"\n📊 Daily Nutritional Summary:")
    output.append(f"   Total Calories: {diet_plan_data['daily_totals']['calories']} cal")
    output.append(f"   Total Protein: {diet_plan_data['daily_totals']['protein']}g")
    
    # Rasa distribution
    output.append(f"\n🎯 Rasa (Six Tastes) Distribution:")
    for rasa, percentage in diet_plan_data['rasa_analysis'].items():
        if percentage > 0:
            output.append(f"   {percentage}% {rasa}")
    
    # AI-Enhanced Analysis
    output.append(f"\n🧘 AI-Enhanced Ayurvedic Analysis:")
    for analysis_point in diet_plan_data['ayurvedic_analysis']:
        output.append(f"   • {analysis_point}")
    
    # Therapeutic notes
    therapeutic = ai_rec.get('therapeutic_notes', '')
    if therapeutic:
        output.append(f"\n💊 Therapeutic Recommendations:")
        output.append(f"   {therapeutic}")
    
    output.append("\n" + "=" * 80)
    output.append("✨ Generated by Hybrid AI-Enhanced AyurDiet Pro v3.0 ✨")
    output.append("🤖 Powered by Google AI Studio (Gemini) + Enhanced Nutrition Algorithm")
    output.append("=" * 80)
    
    return "\n".join(output)