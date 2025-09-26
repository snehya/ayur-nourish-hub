"""
CRITICAL DEMO FIX: Complete Patient Login Setup
This command sets up everything needed for the patient login functionality
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from diet_planner.models import Patient, DietPlan
from datetime import date
import json

User = get_user_model()

class Command(BaseCommand):
    help = '🚨 CRITICAL DEMO FIX: Set up patient login and demo data'

    def handle(self, *args, **options):
        self.stdout.write('🚨 CRITICAL DEMO FIX: PATIENT LOGIN SETUP')
        self.stdout.write('=' * 60)
        
        # Step 1: Create demo users
        self.stdout.write('\n1. 👥 CREATING DEMO USERS')
        
        # Create demo practitioner
        practitioner, created = User.objects.get_or_create(
            username='dr_sharma',
            defaults={
                'email': 'dr.sharma@ayurdiet.com',
                'first_name': 'Rajesh',
                'last_name': 'Sharma',
                'user_type': 'practitioner',
            }
        )
        if created:
            practitioner.set_password('demo123')
            practitioner.save()
            self.stdout.write('   ✅ Created practitioner: dr_sharma')
        else:
            self.stdout.write('   ✅ Practitioner exists: dr_sharma')
        
        # Create demo patient USER
        patient_user, created = User.objects.get_or_create(
            username='patient_ravi',
            defaults={
                'email': 'ravi@example.com',
                'first_name': 'Ravi',
                'last_name': 'Kumar',
                'user_type': 'patient',
            }
        )
        if created:
            patient_user.set_password('demo123')
            patient_user.save()
            self.stdout.write('   ✅ Created patient user: patient_ravi')
        else:
            self.stdout.write('   ✅ Patient user exists: patient_ravi')
        
        # Step 2: Create patient record linked to practitioner
        self.stdout.write('\n2. 📋 CREATING PATIENT RECORDS')
        
        patient_record, created = Patient.objects.get_or_create(
            name='Ravi Kumar',
            defaults={
                'practitioner': practitioner,
                'prakriti': 'Vata-Pitta',
                'vikriti': 'Vata imbalance',
                'agni': 'Variable',
                'health_parameters': 'Weight gain, muscle building, active lifestyle',
            }
        )
        if created:
            self.stdout.write('   ✅ Created patient record: Ravi Kumar')
        else:
            self.stdout.write('   ✅ Patient record exists: Ravi Kumar')
        
        # Step 3: Create a sample diet plan for the patient
        self.stdout.write('\n3. 🍽️ CREATING SAMPLE DIET PLAN')
        
        sample_diet_plan = {
            "breakfast": {
                "foods": [
                    {"food": "Amaranth", "calories": 200, "protein": 7.3, "properties": "(Cooling, Light, Sweet Astringent)"},
                    {"food": "Mung Dal", "calories": 150, "protein": 10.6, "properties": "(Cooling, Easy, Sweet astringent)"},
                    {"food": "Dates", "calories": 100, "protein": 0.6, "properties": "(Neutral, Heavy, Sweet)"}
                ],
                "total_calories": 450,
                "total_protein": 18.5
            },
            "lunch": {
                "foods": [
                    {"food": "Brown Rice", "calories": 250, "protein": 5.9, "properties": "(Neutral, Medium, Sweet)"},
                    {"food": "Spinach", "calories": 50, "protein": 6.3, "properties": "(Cooling, Easy, Bitter Astringent)"},
                    {"food": "Ghee", "calories": 150, "protein": 0.0, "properties": "(Cooling, Easy, Sweet)"}
                ],
                "total_calories": 450,
                "total_protein": 12.2
            },
            "dinner": {
                "foods": [
                    {"food": "Millet", "calories": 200, "protein": 5.8, "properties": "(Neutral, Light, Sweet)"},
                    {"food": "Cashews", "calories": 200, "protein": 6.6, "properties": "(Neutral, Heavy, Sweet)"},
                    {"food": "Almond Milk", "calories": 51, "protein": 1.8, "properties": "(Cooling, Light, Sweet)"}
                ],
                "total_calories": 451,
                "total_protein": 14.2
            },
            "daily_totals": {
                "calories": 1351,
                "protein": 44.9,
                "meals": 3
            },
            "ai_recommendations": {
                "recommended_foods": ["Basmati Rice", "Mung Dal", "Ginger", "Ghee", "Dates"],
                "avoid_foods": ["Cold drinks", "Raw foods", "Processed foods"]
            },
            "ayurvedic_analysis": [
                "Diet plan customized for Vata-Pitta constitution",
                "AI recommendations included for personalized nutrition",
                "Balanced approach for weight gain and muscle building"
            ]
        }
        
        diet_plan, created = DietPlan.objects.get_or_create(
            patient=patient_record,
            plan_date=date.today(),
            defaults={
                'full_plan': sample_diet_plan,
                'breakfast': sample_diet_plan['breakfast'],
                'lunch': sample_diet_plan['lunch'], 
                'dinner': sample_diet_plan['dinner'],
                'practitioner_notes': 'Demo diet plan with AI recommendations for patient login testing'
            }
        )
        if created:
            self.stdout.write('   ✅ Created sample diet plan')
        else:
            self.stdout.write('   ✅ Sample diet plan exists')
        
        # Step 4: Display login credentials
        self.stdout.write('\n' + '='*60)
        self.stdout.write('🎯 DEMO READY! LOGIN CREDENTIALS:')
        self.stdout.write('='*60)
        
        self.stdout.write('\n👨‍⚕️ PRACTITIONER LOGIN:')
        self.stdout.write('   Username: dr_sharma')
        self.stdout.write('   Password: demo123')
        self.stdout.write('   User Type: practitioner')
        
        self.stdout.write('\n👤 PATIENT LOGIN:')
        self.stdout.write('   Username: patient_ravi')
        self.stdout.write('   Password: demo123')
        self.stdout.write('   User Type: patient')
        
        # Step 5: API Endpoints
        self.stdout.write('\n🔗 NEW API ENDPOINTS:')
        self.stdout.write('   • POST /api/auth/login/ (with user_type)')
        self.stdout.write('   • GET  /api/patient/dashboard/ (patient only)')
        self.stdout.write('   • POST /api/patient/feedback/ (patient only)')
        
        # Step 6: Frontend requirements
        self.stdout.write('\n💻 FRONTEND UPDATES NEEDED:')
        self.stdout.write('   1. Add user type dropdown to login form')
        self.stdout.write('   2. Create patient dashboard component')
        self.stdout.write('   3. Add feedback buttons for meals')
        self.stdout.write('   4. Route users based on user_type after login')
        
        self.stdout.write('\n' + '🚨 CRITICAL: Update your frontend login to include user_type!')
        self.stdout.write('🚨 CRITICAL: Test both practitioner and patient logins!')
        self.stdout.write('🚨 CRITICAL: Patient should see their diet plan with feedback buttons!')
        
        self.stdout.write('\n' + '✅ DEMO SETUP COMPLETE!')
        self.stdout.write('='*60)