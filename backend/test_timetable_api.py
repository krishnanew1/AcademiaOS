#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth import get_user_model
from apps.academics.views import TimetablePDFListView
from apps.academics.models import TimetablePDF

User = get_user_model()

# Create test users
print("=== Creating Test Users ===")
admin_user, created = User.objects.get_or_create(
    username='test_admin',
    defaults={'role': 'ADMIN', 'email': 'admin@test.com'}
)
print(f"Admin user: {admin_user.username} (created: {created})")

student_user, created = User.objects.get_or_create(
    username='test_student', 
    defaults={'role': 'STUDENT', 'email': 'student@test.com'}
)
print(f"Student user: {student_user.username} (created: {created})")

faculty_user, created = User.objects.get_or_create(
    username='test_faculty',
    defaults={'role': 'FACULTY', 'email': 'faculty@test.com'}
)
print(f"Faculty user: {faculty_user.username} (created: {created})")

# Test API for each user type
factory = RequestFactory()
view = TimetablePDFListView()

print("\n=== Testing API Responses ===")

for user in [admin_user, student_user, faculty_user]:
    print(f"\n--- Testing for {user.role} user: {user.username} ---")
    
    # Create request
    request = factory.get('/api/academics/timetables/pdfs/')
    request.user = user
    
    # Call view
    response = view.get(request)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Data: {response.data}")
    print(f"Number of timetables returned: {len(response.data) if isinstance(response.data, list) else 'N/A'}")