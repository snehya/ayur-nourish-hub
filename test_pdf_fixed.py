#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ayurdiet_backend.settings')
django.setup()

from api.views import PDFExportView
from diet_planner.models import Patient, DietPlan
from django.http import HttpRequest
from django.contrib.auth.models import User

def test_pdf_generation():
    print('Testing PDF generation...')
    
    # Create a test view instance
    view = PDFExportView()
    print('✓ PDFExportView created successfully')
    
    # Check if we have test data
    patients = Patient.objects.all()
    print(f'Found {patients.count()} patients in database')
    
    if patients.exists():
        patient = patients.first()
        diet_plans = DietPlan.objects.filter(patient=patient)
        print(f'Found {diet_plans.count()} diet plans for patient: {patient.name}')
        
        if diet_plans.exists():
            plan = diet_plans.first()
            print(f'Testing PDF generation for plan ID: {plan.id}')
            
            # Create mock request
            request = HttpRequest()
            request.user = patient.practitioner
            
            try:
                response = view.get(request, plan_id=plan.id)
                print(f'✓ PDF generated successfully! Response type: {type(response).__name__}')
                print(f'✓ Content type: {response.get("Content-Type", "Not set")}')
                print(f'✓ Content length: {len(response.content)} bytes')
                
                # Save test PDF to file
                with open('test_diet_plan.pdf', 'wb') as f:
                    f.write(response.content)
                print('✓ Test PDF saved as test_diet_plan.pdf')
                
            except Exception as e:
                print(f'✗ Error generating PDF: {e}')
                import traceback
                traceback.print_exc()
        else:
            print('No diet plans found for testing')
    else:
        print('No patients found for testing')

if __name__ == '__main__':
    test_pdf_generation()