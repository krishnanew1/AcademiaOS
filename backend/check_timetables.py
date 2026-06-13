#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.academics.models import TimetablePDF

print("=== Timetable Database Check ===")
print(f"Total TimetablePDF records: {TimetablePDF.objects.count()}")
print(f"Active TimetablePDF records: {TimetablePDF.objects.filter(is_active=True).count()}")

print("\n=== All Timetables ===")
for t in TimetablePDF.objects.all():
    print(f"ID: {t.id}")
    print(f"  Title: {t.title}")
    print(f"  Academic Year: {t.academic_year}")
    print(f"  Active: {t.is_active}")
    print(f"  Department: {t.department}")
    print(f"  PDF File: {t.pdf_file}")
    print(f"  Created: {t.created_at}")
    print("---")