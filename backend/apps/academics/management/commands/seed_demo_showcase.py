"""
Seed a coherent synthetic showcase dataset for the public read-only demo.

All names, IDs and records are fictional. Idempotent: safe to run twice.
Requires seed_data (demo users) to have run first.
"""
import datetime
import random

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.users.models import CustomUser, StudentProfile, FacultyProfile
from apps.academics.models import Department, Program, Course, Subject, Timetable
from apps.students.models import SemesterRegistration, RegisteredCourse, Enrollment
from apps.attendance.models import Attendance
from apps.exams.models import StudentGrade


class Command(BaseCommand):
    help = 'Populate coherent synthetic data so the read-only demo shows real features'

    def handle(self, *args, **options):
        random.seed(42)
        # Ensure departments/programs/subjects exist (synthetic catalog).
        call_command('seed_real_data')

        cse = Department.objects.filter(code__iexact='CSE').first() or Department.objects.first()
        btech_cse = (Course.objects.filter(code__iexact='BTECH-CSE').first()
                     or Course.objects.filter(code__iexact='BTECHCSE').first()
                     or Course.objects.filter(code__icontains='BTECH', department__code__iexact='CSE').first())
        if not btech_cse:
            self.stdout.write(self.style.ERROR('BTECH-CSE course missing after seed_real_data'))
            return
        program = btech_cse.program if hasattr(btech_cse, 'program') else None

        # --- Student profile: john_doe -> coherent B.Tech CSE student ---
        student_user = CustomUser.objects.get(username='john_doe')
        sp = student_user.student_profile
        sp.reg_no = '2024BCS042'
        sp.enrollment_number = '2024BCS042'
        sp.department = cse
        if program:
            sp.program = program
        sp.current_semester = 3
        sp.batch_year = 2024
        sp.phone = '+91-9000000001'
        sp.save()

        if not Enrollment.objects.filter(student=sp, course=btech_cse, semester=3).exists():
            Enrollment.objects.create(student=sp, course=btech_cse, semester=3, status='Active')

        # --- Faculty: prof_smith + one colleague, both CSE ---
        prof_user = CustomUser.objects.get(username='prof_smith')
        fp = prof_user.faculty_profile
        fp.department = cse
        fp.designation = 'Assistant Professor'
        fp.specialization = 'Data Structures and Algorithms'
        fp.save()

        mehta_user, _ = CustomUser.objects.get_or_create(
            username='dr_mehta',
            defaults={'email': 'mehta@example.edu', 'role': 'FACULTY',
                      'first_name': 'Anjali', 'last_name': 'Mehta'},
        )
        mehta, _ = FacultyProfile.objects.get_or_create(
            user=mehta_user,
            defaults={'employee_id': 'FAC-CSE-014', 'department': cse,
                      'designation': 'Associate Professor',
                      'specialization': 'Database Systems'},
        )

        # --- Subjects for semester 3 (current) and 1-2 (completed) ---
        sem3 = list(Subject.objects.filter(course=btech_cse, semester=3)[:5])
        sem1 = list(Subject.objects.filter(course=btech_cse, semester=1)[:5])
        sem2 = list(Subject.objects.filter(course=btech_cse, semester=2)[:5])
        if len(sem3) < 3:
            self.stdout.write(self.style.ERROR('Not enough semester-3 subjects in catalog'))
            return
        # Assign faculty to current subjects (alternate).
        for i, sub in enumerate(sem3):
            sub.faculty = fp if i % 2 == 0 else mehta
            sub.save()

        # --- Approved semester registration with registered courses ---
        reg, _ = SemesterRegistration.objects.get_or_create(
            student=sp, academic_year='2025-26', semester='Jul-Dec 2026',
            defaults={'institute_fee_paid': True, 'hostel_fee_paid': True,
                      'hostel_room_no': 'H-3/214', 'approval_status': 'approved',
                      'approved_at': timezone.now(),
                      'total_credits': sum(s.credits or 3 for s in sem3)},
        )
        for sub in sem3:
            RegisteredCourse.objects.get_or_create(semester_registration=reg, subject=sub)

        # --- Past grades: semesters 1 and 2 completed ---
        scale = [('A', 92), ('A-', 85), ('B', 78), ('B-', 72), ('A', 90)]
        for term_subjects in (sem1, sem2):
            for i, sub in enumerate(term_subjects):
                letter, marks = scale[(i + (0 if sub in sem1 else 2)) % len(scale)]
                StudentGrade.objects.get_or_create(
                    student=sp, subject=sub,
                    defaults={'faculty': fp, 'marks_obtained': marks,
                              'total_marks': 100, 'grade_letter': letter},
                )

        # --- Attendance for current subjects over recent weeks ---
        today = timezone.now().date()
        days = [today - datetime.timedelta(days=d) for d in range(1, 29)]
        weekdays = [d for d in days if d.weekday() < 5]
        for sub in sem3:
            marker = sub.faculty.user if sub.faculty else prof_user
            for d in weekdays[::2]:  # roughly alternate class days
                Attendance.objects.get_or_create(
                    student=sp, subject=sub, date=d,
                    defaults={'status': 'Present' if random.random() > 0.12 else 'Absent',
                              'recorded_by': marker},
                )

        # --- Timetable for current subjects ---
        slot_times = [(datetime.time(9, 0), datetime.time(9, 55)),
                      (datetime.time(10, 0), datetime.time(10, 55)),
                      (datetime.time(11, 5), datetime.time(12, 0)),
                      (datetime.time(13, 0), datetime.time(13, 55)),
                      (datetime.time(14, 0), datetime.time(14, 55))]
        days_of_week = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY']
        for i, sub in enumerate(sem3):
            st, et = slot_times[i % len(slot_times)]
            Timetable.objects.get_or_create(
                class_name='CSE-A', subject=sub, day_of_week=days_of_week[i % 5],
                start_time=st,
                defaults={'faculty': sub.faculty, 'end_time': et,
                          'room_number': f'LT-{i + 1}01', 'academic_year': '2025-26',
                          'is_active': True},
            )

        self.stdout.write(self.style.SUCCESS(
            f'Showcase seeded: {len(sem3)} current subjects, '
            f'{len(sem1) + len(sem2)} past grades, '
            f'{Attendance.objects.filter(student=sp).count()} attendance records, '
            f'{Timetable.objects.filter(class_name="CSE-A").count()} timetable entries.'
        ))
