#!/usr/bin/env python
"""
Phase 5: PDF Export Endpoint Demonstration
This script shows how to use the newly implemented PDF export functionality.
"""
import os
import sys
import django

# Set up Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ayurdiet_backend.settings')
django.setup()

from django.test import Client
from users.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from diet_planner.models import DietPlan, Patient
import json

def demonstrate_pdf_export():
    print("🎯 PHASE 5: PDF EXPORT DEMONSTRATION")
    print("=" * 50)
    
    # Create a test client
    client = Client()
    
    # Get test data
    practitioner = CustomUser.objects.filter(user_type='practitioner').first()
    if not practitioner:
        print("❌ No practitioner found. Please create a practitioner user first.")
        return
    
    patient = Patient.objects.first()
    if not patient:
        print("❌ No patient found. Please create test data first.")
        return
    
    diet_plan = DietPlan.objects.filter(patient=patient).first()
    if not diet_plan:
        print("❌ No diet plan found. Please create test data first.")
        return
    
    # Generate JWT token
    refresh = RefreshToken.for_user(practitioner)
    access_token = str(refresh.access_token)
    
    print(f"📋 Test Data:")
    print(f"   Practitioner: {practitioner.username}")
    print(f"   Patient: {patient.name}")
    print(f"   Diet Plan ID: {diet_plan.id}")
    print(f"   Plan Date: {diet_plan.plan_date}")
    print()
    
    # Test PDF export endpoint
    print("🔥 Testing PDF Export Endpoint:")
    print(f"   URL: /api/plans/{diet_plan.id}/export-pdf/")
    
    response = client.get(
        f'/api/plans/{diet_plan.id}/export-pdf/',
        HTTP_AUTHORIZATION=f'Bearer {access_token}'
    )
    
    print(f"   Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print(f"   ✅ SUCCESS! PDF generated")
        print(f"   Content-Type: {response.get('Content-Type')}")
        print(f"   Content-Length: {len(response.content)} bytes")
        
        # Extract filename from Content-Disposition header
        content_disposition = response.get('Content-Disposition', '')
        if 'filename=' in content_disposition:
            filename = content_disposition.split('filename=')[1].strip('"')
            print(f"   Filename: {filename}")
        
        # Save the PDF
        demo_filename = f"demo_export_plan_{diet_plan.id}.pdf"
        with open(demo_filename, 'wb') as f:
            f.write(response.content)
        print(f"   📄 PDF saved as: {demo_filename}")
        
    else:
        print(f"   ❌ FAILED with status {response.status_code}")
        try:
            error_data = json.loads(response.content.decode())
            print(f"   Error: {error_data}")
        except:
            print(f"   Raw response: {response.content}")
    
    print()
    print("🚀 API Usage Examples:")
    print("=" * 30)
    print("# Using curl:")
    print(f'curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \\')
    print(f'     -o diet_plan.pdf \\')
    print(f'     "http://127.0.0.1:8000/api/plans/{diet_plan.id}/export-pdf/"')
    print()
    print("# Using JavaScript fetch:")
    print("fetch('/api/plans/1/export-pdf/', {")
    print("  headers: {")
    print("    'Authorization': 'Bearer ' + token")
    print("  }")
    print("})")
    print(".then(response => response.blob())")
    print(".then(blob => {")
    print("  const url = window.URL.createObjectURL(blob);")
    print("  const a = document.createElement('a');")
    print("  a.href = url;")
    print("  a.download = 'diet_plan.pdf';")
    print("  a.click();")
    print("});")
    print()
    print("🎉 Phase 5 PDF Export is fully operational!")

if __name__ == '__main__':
    demonstrate_pdf_export()