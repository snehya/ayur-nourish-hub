#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(r'C:\Users\sneha\ayurdiet_backend')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ayurdiet_backend.settings')
django.setup()

from users.models import CustomUser

print("🔐 Creating test user for JWT authentication...")

# Create or update a test user with known credentials
test_user, created = CustomUser.objects.get_or_create(
    username='testuser',
    defaults={
        'email': 'test@ayurdiet.com',
        'user_type': 'practitioner',
        'first_name': 'Test',
        'last_name': 'User'
    }
)

# Set a known password
test_user.set_password('testpass123')
test_user.save()

if created:
    print("✅ Created new test user")
else:
    print("✅ Updated existing test user password")

print(f"   Username: testuser")
print(f"   Password: testpass123")
print(f"   User Type: {test_user.user_type}")
print(f"   Email: {test_user.email}")

print("\n🎯 You can now test JWT authentication with these credentials")
print("   Start server: python manage.py runserver")
print("   Test endpoint: POST http://127.0.0.1:8000/api/token/")
print("   JSON payload: {\"username\": \"testuser\", \"password\": \"testpass123\"}")