"""
Test script to evaluate the enhanced hybrid AI system with comprehensive food dataset
This will demonstrate improved variety, nutrition, and AI personalization
"""

import sys
import os
import django

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ayurdiet_backend.settings')
django.setup()

from diet_planner.hybrid_ai_diet_generator import HybridAIAyurvedicDietGenerator
from diet_planner.models import Food

def test_comprehensive_dataset():
    """Test the hybrid AI system with the expanded 115-food dataset"""
    
    print("🌟 TESTING HYBRID AI SYSTEM WITH COMPREHENSIVE DATASET")
    print("=" * 70)
    
    # Check food count
    total_foods = Food.objects.count()
    print(f"📊 Total foods available: {total_foods}")
    
    # Sample different food categories
    categories = Food.objects.values_list('food_category', flat=True).distinct()
    print(f"🥗 Food categories: {list(categories)}")
    
    # Create a test patient object
    class TestPatient:
        def __init__(self):
            self.prakriti = 'Vata-Pitta'
            self.vikriti = 'Vata imbalance'
            self.agni = 'Variable'
            self.health_parameters = 'Weight gain, muscle building, active lifestyle'
            self.age = 28
            self.gender = 'Male'
            self.target_calories = 2000
            self.target_protein = 70
    
    test_patient = TestPatient()
    
    print(f"\n🎯 Test Patient Profile:")
    print(f"   • Prakriti: {test_patient.prakriti}")
    print(f"   • Vikriti: {test_patient.vikriti}")
    print(f"   • Agni: {test_patient.agni}")
    print(f"   • Health Goals: {test_patient.health_parameters}")
    print(f"   • Target: {test_patient.target_calories} cal, {test_patient.target_protein}g protein")
    
    # Initialize hybrid AI generator
    generator = HybridAIAyurvedicDietGenerator()
    
    print(f"\n🤖 Generating AI-enhanced diet plan...")
    print("-" * 50)
    
    try:
        # Generate diet plan
        diet_plan = generator.generate_hybrid_diet_plan(test_patient)
        
        # Analyze results - first let's see the structure
        print(f"\n✨ DIET PLAN GENERATED SUCCESSFULLY!")
        print("=" * 50)
        
        # Debug: Show the structure
        print(f"\n🔍 Diet Plan Structure:")
        print(f"   Type: {type(diet_plan)}")
        print(f"   Keys: {list(diet_plan.keys()) if isinstance(diet_plan, dict) else 'Not a dict'}")
        
        total_calories = 0
        total_protein = 0
        unique_foods = set()
        
        # Analyze meals with correct structure
        for meal_name in ['breakfast', 'lunch', 'dinner']:
            if meal_name in diet_plan:
                meal_data = diet_plan[meal_name]
                print(f"\n🍽️  {meal_name.upper()}:")
                
                meal_calories = 0
                meal_protein = 0
                
                # Handle the new structure with 'foods' array
                foods_list = meal_data.get('foods', [])
                for item in foods_list:
                    food_obj = item['food']
                    food_name = food_obj.name
                    calories = item['calories']
                    protein = item['protein']
                    properties = item.get('properties', '')
                    
                    print(f"   • {food_name} - {calories} cal, {protein}g protein {properties}")
                    
                    meal_calories += calories
                    meal_protein += protein
                    unique_foods.add(food_name)
                
                print(f"   � Meal Total: {meal_calories} calories, {meal_protein:.1f}g protein")
                total_calories += meal_calories
                total_protein += meal_protein
        
        # Display daily totals from the system
        if 'daily_totals' in diet_plan:
            daily_data = diet_plan['daily_totals']
            print(f"\n📊 DAILY TOTALS (From System):")
            print(f"   • Calories: {daily_data.get('calories', 0)}")
            print(f"   • Protein: {daily_data.get('protein', 0):.1f}g")
            print(f"   • Meals: {daily_data.get('meals', 0)}")
        
        # Display AI recommendations if available
        if 'ai_recommendations' in diet_plan:
            print(f"\n🤖 AI PERSONALIZED RECOMMENDATIONS:")
            print("-" * 40)
            ai_data = diet_plan['ai_recommendations']
            
            if 'recommended_foods' in ai_data:
                print(f"   ✅ Recommended: {', '.join(ai_data['recommended_foods'][:5])}")
            if 'avoid_foods' in ai_data:
                print(f"   ❌ Avoid: {', '.join(ai_data['avoid_foods'][:3])}")
        
        # Ayurvedic analysis
        if 'ayurvedic_analysis' in diet_plan:
            print(f"\n🌿 AYURVEDIC ANALYSIS:")
            for analysis in diet_plan['ayurvedic_analysis'][:3]:
                print(f"   • {analysis}")
        
        # Rasa distribution
        if 'rasa_analysis' in diet_plan:
            print(f"\n🍃 RASA DISTRIBUTION:")
            rasa_data = diet_plan['rasa_analysis']
            for rasa, percentage in rasa_data.items():
                if percentage > 0:
                    print(f"   • {rasa}: {percentage}%")
        
        # Final analysis
        print(f"\n📈 COMPREHENSIVE ANALYSIS:")
        print("=" * 50)
        print(f"🎯 Total Calories: {total_calories} (Target: {test_patient.target_calories})")
        print(f"💪 Total Protein: {total_protein:.1f}g (Target: {test_patient.target_protein}g)")
        print(f"🌈 Unique Foods: {len(unique_foods)} foods")
        print(f"📊 Food Variety: {', '.join(sorted(list(unique_foods)))}")
        
        # Performance metrics
        calorie_accuracy = abs(total_calories - test_patient.target_calories) / test_patient.target_calories * 100
        protein_accuracy = abs(total_protein - test_patient.target_protein) / test_patient.target_protein * 100
        
        print(f"\n🎯 PERFORMANCE METRICS:")
        print(f"   • Calorie Accuracy: {100-calorie_accuracy:.1f}%")
        print(f"   • Protein Accuracy: {100-protein_accuracy:.1f}%")
        print(f"   • Food Diversity: {len(unique_foods)} unique items")
        print(f"   • AI Enhancement: {'✅ Active' if 'ai_recommendations' in diet_plan else '❌ Inactive'}")
        
        # Database utilization
        utilization = (len(unique_foods) / total_foods) * 100
        print(f"   • Database Utilization: {utilization:.1f}% ({len(unique_foods)}/{total_foods} foods)")
        
        print(f"\n� SYSTEM STATUS: {'🎉 EXCELLENT PERFORMANCE!' if len(unique_foods) >= 10 and calorie_accuracy < 10 else '✅ Good Performance'}")
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_comprehensive_dataset()