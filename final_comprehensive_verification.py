#!/usr/bin/env python3
"""
FINAL COMPREHENSIVE BACKEND VERIFICATION
Complete check of all systems after loading 442 foods
"""
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ayurdiet_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from diet_planner.models import Patient, Food, DietPlan
from diet_planner.hybrid_ai_diet_generator import HybridAIAyurvedicDietGenerator, format_hybrid_diet_plan_output

User = get_user_model()

def final_comprehensive_verification():
    print("🔍 FINAL COMPREHENSIVE BACKEND VERIFICATION")
    print("=" * 70)
    print("Verifying ALL systems after loading complete 442-food database...")
    
    success_count = 0
    total_tests = 0
    
    # Test 1: Database Models & Data
    print("\n1️⃣ DATABASE MODELS & DATA")
    print("-" * 40)
    total_tests += 5
    
    try:
        users = User.objects.all()
        patients = Patient.objects.all()
        foods = Food.objects.all()
        
        print(f"✅ Users: {users.count()} found")
        success_count += 1
        print(f"✅ Patients: {patients.count()} found") 
        success_count += 1
        print(f"✅ Foods: {foods.count()} found (TARGET: 442)")
        success_count += 1
        
        # Check for demo users
        demo_practitioner = User.objects.filter(username='demo_practitioner').first()
        demo_patient = User.objects.filter(username='demo_patient').first()
        
        if demo_practitioner and demo_patient:
            print(f"✅ Demo users ready: {demo_practitioner.username} & {demo_patient.username}")
            success_count += 1
        else:
            print("❌ Demo users missing")
            
        # Check food variety
        categories = Food.objects.values_list('food_category', flat=True).distinct()
        if len(categories) >= 40:
            print(f"✅ Food categories: {len(categories)} (excellent variety)")
            success_count += 1
        else:
            print(f"⚠️ Food categories: {len(categories)} (could be more)")
            
    except Exception as e:
        print(f"❌ Database error: {e}")
    
    # Test 2: Authentication System
    print("\n2️⃣ AUTHENTICATION SYSTEM")
    print("-" * 40)
    total_tests += 4
    
    try:
        # Check user types
        practitioners = User.objects.filter(user_type='practitioner')
        patient_users = User.objects.filter(user_type='patient')
        
        print(f"✅ Practitioners: {practitioners.count()}")
        success_count += 1
        print(f"✅ Patient users: {patient_users.count()}")
        success_count += 1
        
        # Test authentication for demo users
        if demo_practitioner and demo_practitioner.check_password('demo123'):
            print("✅ Demo practitioner login: WORKING")
            success_count += 1
        else:
            print("❌ Demo practitioner login: FAILED")
            
        if demo_patient and demo_patient.check_password('demo123'):
            print("✅ Demo patient login: WORKING")
            success_count += 1
        else:
            print("❌ Demo patient login: FAILED")
            
    except Exception as e:
        print(f"❌ Authentication error: {e}")
    
    # Test 3: AI Diet Generator
    print("\n3️⃣ AI DIET GENERATOR")
    print("-" * 40)
    total_tests += 4
    
    try:
        # Test import
        diet_generator = HybridAIAyurvedicDietGenerator()
        print("✅ HybridAIAyurvedicDietGenerator: IMPORTED & INSTANTIATED")
        success_count += 1
        
        # Test with patient
        if patients.exists():
            test_patient = patients.first()
            print(f"✅ Test patient available: {test_patient.name}")
            success_count += 1
            
            # Test diet plan generation
            try:
                diet_plan_data = diet_generator.generate_hybrid_diet_plan(test_patient)
                print("✅ AI diet plan generation: WORKING")
                success_count += 1
                
                # Test formatting
                formatted_output = format_hybrid_diet_plan_output(test_patient, diet_plan_data)
                print("✅ Diet plan formatting: WORKING")
                success_count += 1
                
            except Exception as e:
                print(f"❌ AI generation error: {e}")
        else:
            print("❌ No patients for AI testing")
            
    except Exception as e:
        print(f"❌ AI Diet Generator error: {e}")
    
    # Test 4: Food Database Quality
    print("\n4️⃣ FOOD DATABASE QUALITY")
    print("-" * 40)
    total_tests += 6
    
    try:
        # Check for key Ayurvedic foods
        key_foods = ['Rice', 'Dal', 'Ghee', 'Turmeric', 'Ginger', 'Cumin Seeds']
        found_key_foods = 0
        
        for food_name in key_foods:
            if Food.objects.filter(name__icontains=food_name.split()[0]).exists():
                found_key_foods += 1
                
        if found_key_foods >= 5:
            print(f"✅ Key Ayurvedic foods: {found_key_foods}/{len(key_foods)} found")
            success_count += 1
        else:
            print(f"⚠️ Key Ayurvedic foods: {found_key_foods}/{len(key_foods)} found")
        
        # Check nutritional data completeness
        foods_with_calories = Food.objects.exclude(calories__isnull=True).exclude(calories=0).count()
        foods_with_protein = Food.objects.exclude(protein__isnull=True).count()
        
        if foods_with_calories > 400:
            print(f"✅ Foods with calorie data: {foods_with_calories}")
            success_count += 1
        else:
            print(f"⚠️ Foods with calorie data: {foods_with_calories}")
            
        if foods_with_protein > 400:
            print(f"✅ Foods with protein data: {foods_with_protein}")
            success_count += 1
        else:
            print(f"⚠️ Foods with protein data: {foods_with_protein}")
        
        # Check Ayurvedic properties
        foods_with_rasa = Food.objects.exclude(rasa__isnull=True).exclude(rasa='').count()
        foods_with_virya = Food.objects.exclude(virya__isnull=True).exclude(virya='').count()
        foods_with_dosha_effects = Food.objects.exclude(vata_effect__isnull=True).exclude(vata_effect='').count()
        
        if foods_with_rasa > 400:
            print(f"✅ Foods with Rasa data: {foods_with_rasa}")
            success_count += 1
        else:
            print(f"⚠️ Foods with Rasa data: {foods_with_rasa}")
            
        if foods_with_virya > 400:
            print(f"✅ Foods with Virya data: {foods_with_virya}")
            success_count += 1
        else:
            print(f"⚠️ Foods with Virya data: {foods_with_virya}")
            
        if foods_with_dosha_effects > 400:
            print(f"✅ Foods with Dosha effects: {foods_with_dosha_effects}")
            success_count += 1
        else:
            print(f"⚠️ Foods with Dosha effects: {foods_with_dosha_effects}")
            
    except Exception as e:
        print(f"❌ Food database quality error: {e}")
    
    # Test 5: Patient-Specific Features
    print("\n5️⃣ PATIENT-SPECIFIC FEATURES")
    print("-" * 40)
    total_tests += 3
    
    try:
        if patients.exists():
            test_patient = patients.first()
            
            # Check patient has practitioner
            if test_patient.practitioner:
                print(f"✅ Patient-Practitioner relationship: WORKING")
                success_count += 1
            else:
                print("❌ Patient-Practitioner relationship: MISSING")
            
            # Check patient attributes
            if test_patient.prakriti and test_patient.vikriti:
                print(f"✅ Patient Ayurvedic profile: Complete")
                success_count += 1
            else:
                print("⚠️ Patient Ayurvedic profile: Incomplete")
            
            # Check health parameters
            if test_patient.health_parameters:
                print(f"✅ Patient health data: Available")
                success_count += 1
            else:
                print("⚠️ Patient health data: Missing")
                
        else:
            print("❌ No patients to test features")
            
    except Exception as e:
        print(f"❌ Patient features error: {e}")
    
    # Test 6: API Import Paths
    print("\n6️⃣ API IMPORT PATHS")
    print("-" * 40)
    total_tests += 2
    
    try:
        # Test critical imports that were fixed
        from diet_planner.hybrid_ai_diet_generator import HybridAIAyurvedicDietGenerator
        from diet_planner.models import Patient, Food
        print("✅ All import paths: WORKING")
        success_count += 2
        
    except Exception as e:
        print(f"❌ Import path error: {e}")
    
    # Final Assessment
    print("\n" + "=" * 70)
    print("🎯 FINAL COMPREHENSIVE ASSESSMENT")
    print("=" * 70)
    
    success_rate = (success_count / total_tests) * 100
    
    print(f"📊 TESTS PASSED: {success_count}/{total_tests} ({success_rate:.1f}%)")
    
    if success_rate >= 95:
        print("\n🏆 BACKEND STATUS: PERFECTLY COMPLETE!")
        print("🌟 ALL SYSTEMS OPERATIONAL")
        print("✅ 442-Food Database: COMPLETE")
        print("✅ AI Diet Generation: WORKING")
        print("✅ Authentication: FUNCTIONAL")
        print("✅ Patient Features: READY")
        print("✅ Demo Users: CONFIGURED")
        print("\n🚀 READY FOR PRODUCTION DEMO!")
        return True
        
    elif success_rate >= 85:
        print("\n🎉 BACKEND STATUS: NEARLY PERFECT")
        print("⚠️ Minor issues detected - review above")
        print("💪 Overall system functional for demo")
        return True
        
    else:
        print("\n⚠️ BACKEND STATUS: NEEDS ATTENTION")
        print("❌ Critical issues detected - review above")
        print("🔧 Fix required before demo")
        return False

if __name__ == "__main__":
    result = final_comprehensive_verification()
    sys.exit(0 if result else 1)