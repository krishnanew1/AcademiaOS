#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import CustomUser

print("=== User Profile Analysis ===")

users = CustomUser.objects.filter(role__in=['STUDENT', 'FACULTY'])

for user in users:
    print(f"\nUser: {user.username} ({user.role})")
    
    if user.role == 'STUDENT':
        if hasattr(user, 'student_profile'):
            profile = user.student_profile
            print(f"  Has student profile: YES")
            print(f"  Department: {profile.department}")
            print(f"  Reg No: {profile.reg_no}")
            print(f"  Program: {profile.program}")
        else:
            print(f"  Has student profile: NO")
    
    elif user.role == 'FACULTY':
        if hasattr(user, 'faculty_profile'):
            profile = user.faculty_profile
            print(f"  Has faculty profile: YES")
            print(f"  Department: {profile.department}")
            print(f"  Employee ID: {profile.employee_id}")
        else:
            print(f"  Has faculty profile: NO")

print("\n=== Creating Missing Profiles ===")

# Check if we need to create profiles for users without them
from apps.academics.models import Department

# Get a default department
default_dept = Department.objects.first()
print(f"Default department: {default_dept}")

for user in users:
    if user.role == 'STUDENT' and not hasattr(user, 'student_profile'):
        print(f"Creating student profile for {user.username}")
        from apps.students.models import StudentProfile
        StudentProfile.objects.create(
            user=user,
            reg_no=f"TEST_{user.username}",
            department=default_dept
        )
    
    elif user.role == 'FACULTY' and not hasattr(user, 'faculty_profile'):
        print(f"Creating faculty profile for {user.username}")
        from apps.faculty.models import FacultyProfile
        FacultyProfile.objects.create(
            user=user,
            employee_id=f"EMP_{user.username}",
            department=default_dept
        )