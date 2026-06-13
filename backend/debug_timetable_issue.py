#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.academics.models import TimetablePDF, Department
from apps.users.models import CustomUser
from django.db import models

print("=== Debugging Timetable Visibility Issue ===")

# Check existing users
print("\n=== Existing Users ===")
users = CustomUser.objects.all()
for user in users:
    print(f"User: {user.username} | Role: {user.role}")
    if user.role == 'STUDENT' and hasattr(user, 'student_profile'):
        print(f"  Student Department: {user.student_profile.department}")
    elif user.role == 'FACULTY' and hasattr(user, 'faculty_profile'):
        print(f"  Faculty Department: {user.faculty_profile.department}")

print("\n=== Timetables and Department Filtering ===")
timetables = TimetablePDF.objects.filter(is_active=True)
for t in timetables:
    print(f"Timetable: {t.title}")
    print(f"  Department: {t.department}")
    print(f"  Academic Year: {t.academic_year}")
    
    # Check what users should see this timetable
    if t.department is None:
        print("  → Visible to ALL users (institution-wide)")
    else:
        print(f"  → Visible to users in department: {t.department}")
        
        # Find users in this department
        students_in_dept = CustomUser.objects.filter(
            role='STUDENT',
            student_profile__department=t.department
        )
        faculty_in_dept = CustomUser.objects.filter(
            role='FACULTY', 
            faculty_profile__department=t.department
        )
        
        print(f"    Students in this dept: {[u.username for u in students_in_dept]}")
        print(f"    Faculty in this dept: {[u.username for u in faculty_in_dept]}")
    print("---")

print("\n=== Department Analysis ===")
departments = Department.objects.all()
for dept in departments:
    print(f"Department: {dept.name} ({dept.code})")
    student_count = CustomUser.objects.filter(
        role='STUDENT',
        student_profile__department=dept
    ).count()
    faculty_count = CustomUser.objects.filter(
        role='FACULTY',
        faculty_profile__department=dept
    ).count()
    print(f"  Students: {student_count}")
    print(f"  Faculty: {faculty_count}")

print("\n=== Simulating API Logic ===")
# Simulate the API filtering logic for each user
for user in CustomUser.objects.filter(role__in=['STUDENT', 'FACULTY']):
    print(f"\nUser: {user.username} ({user.role})")
    
    # Get user's department
    user_department = None
    if user.role == 'STUDENT' and hasattr(user, 'student_profile'):
        user_department = user.student_profile.department
    elif user.role == 'FACULTY' and hasattr(user, 'faculty_profile'):
        user_department = user.faculty_profile.department
    
    print(f"  User Department: {user_department}")
    
    # Apply filtering logic from the API
    queryset = TimetablePDF.objects.filter(is_active=True)
    
    if user_department:
        # Show timetables for user's department or institution-wide (null department)
        filtered_queryset = queryset.filter(
            models.Q(department=user_department) | models.Q(department__isnull=True)
        )
    else:
        # Show only institution-wide timetables
        filtered_queryset = queryset.filter(department__isnull=True)
    
    print(f"  Timetables visible: {[t.title for t in filtered_queryset]}")
    print(f"  Count: {filtered_queryset.count()}")