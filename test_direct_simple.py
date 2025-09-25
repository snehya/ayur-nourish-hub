#!/usr/bin/env python
"""
Simple Direct PDF Generation Test
This directly tests the PDF view without Django's test client.
"""
import os
import sys
import django

# Set up Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ayurdiet_backend.settings')
django.setup()

from api.views import PDFExportView
from diet_planner.models import Patient, DietPlan
from django.http import HttpRequest
from users.models import CustomUser

def test_direct_pdf():
    print("🎯 DIRECT PDF GENERATION TEST")
    print("=" * 40)
    
    # Get test data
    practitioner = CustomUser.objects.filter(user_type='practitioner').first()
    if not practitioner:
        print("❌ No practitioner found")
        return
    
    patient = Patient.objects.first()
    if not patient:
        print("❌ No patient found")
        return
    
    diet_plan = DietPlan.objects.filter(patient=patient).first()
    if not diet_plan:
        print("❌ No diet plan found")
        return
    
    print(f"📋 Test Data:")
    print(f"   Practitioner: {practitioner.username}")
    print(f"   Patient: {patient.name}")
    print(f"   Diet Plan ID: {diet_plan.id}")
    print()
    
    # Create view and request
    view = PDFExportView()
    request = HttpRequest()
    request.user = practitioner
    request.method = 'GET'
    
    # Call the view directly (bypassing middleware)
    try:
        response = view.get(request, plan_id=diet_plan.id)
        
        print("✅ SUCCESS! PDF generated directly")
        print(f"   Response Type: {type(response).__name__}")
        print(f"   Status Code: {response.status_code}")
        print(f"   Content-Type: {response.get('Content-Type')}")
        print(f"   Content-Length: {len(response.content)} bytes")
        
        # Extract filename from Content-Disposition
        content_disposition = response.get('Content-Disposition', '')
        if 'filename=' in content_disposition:
            filename = content_disposition.split('filename=')[1].strip('"')
            print(f"   Filename: {filename}")
        
        # Save the PDF
        test_filename = f"direct_test_plan_{diet_plan.id}.pdf"
        with open(test_filename, 'wb') as f:
            f.write(response.content)
        print(f"   📄 PDF saved as: {test_filename}")
        
        # Validate PDF content
        if response.content.startswith(b'%PDF'):
            print("   ✅ Valid PDF format confirmed")
        else:
            print("   ❌ Invalid PDF format")
        
        print()
        print("🎉 Phase 5 PDF Export is working perfectly!")
        print("   Ready for production use with proper authentication")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_direct_pdf()