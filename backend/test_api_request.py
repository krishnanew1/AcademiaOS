#!/usr/bin/env python
import requests
import json

# Test the timetable API endpoint
base_url = "http://127.0.0.1:8000"

# First, let's try to login to get a token
login_data = {
    "username": "Aksh",  # Student user
    "password": "Student@2026"
}

print("=== Testing Timetable API ===")

try:
    # Login to get token
    print("1. Logging in as student 'Aksh'...")
    login_response = requests.post(f"{base_url}/api/auth/login/", json=login_data)
    print(f"Login Status: {login_response.status_code}")
    
    if login_response.status_code == 200:
        token_data = login_response.json()
        access_token = token_data.get('access')
        print(f"Access token obtained: {access_token[:50]}...")
        
        # Test timetable endpoint
        print("\n2. Fetching timetables...")
        headers = {"Authorization": f"Bearer {access_token}"}
        timetable_response = requests.get(f"{base_url}/api/academics/timetables/pdfs/", headers=headers)
        
        print(f"Timetable API Status: {timetable_response.status_code}")
        print(f"Response Headers: {dict(timetable_response.headers)}")
        
        if timetable_response.status_code == 200:
            timetables = timetable_response.json()
            print(f"Number of timetables returned: {len(timetables)}")
            print("Timetables:")
            for i, t in enumerate(timetables):
                print(f"  {i+1}. {t.get('title')} ({t.get('academic_year')})")
                print(f"     Department: {t.get('department_name', 'All Departments')}")
                print(f"     PDF URL: {t.get('pdf_url', 'No URL')}")
        else:
            print(f"Error response: {timetable_response.text}")
    else:
        print(f"Login failed: {login_response.text}")

except Exception as e:
    print(f"Error: {e}")

print("\n=== Testing with Faculty User ===")

# Test with faculty user
faculty_login_data = {
    "username": "aj_k",  # Faculty user
    "password": "Faculty@2026"
}

try:
    # Login to get token
    print("1. Logging in as faculty 'aj_k'...")
    login_response = requests.post(f"{base_url}/api/auth/login/", json=faculty_login_data)
    print(f"Login Status: {login_response.status_code}")
    
    if login_response.status_code == 200:
        token_data = login_response.json()
        access_token = token_data.get('access')
        print(f"Access token obtained: {access_token[:50]}...")
        
        # Test timetable endpoint
        print("\n2. Fetching timetables...")
        headers = {"Authorization": f"Bearer {access_token}"}
        timetable_response = requests.get(f"{base_url}/api/academics/timetables/pdfs/", headers=headers)
        
        print(f"Timetable API Status: {timetable_response.status_code}")
        
        if timetable_response.status_code == 200:
            timetables = timetable_response.json()
            print(f"Number of timetables returned: {len(timetables)}")
            print("Timetables:")
            for i, t in enumerate(timetables):
                print(f"  {i+1}. {t.get('title')} ({t.get('academic_year')})")
                print(f"     Department: {t.get('department_name', 'All Departments')}")
                print(f"     PDF URL: {t.get('pdf_url', 'No URL')}")
        else:
            print(f"Error response: {timetable_response.text}")
    else:
        print(f"Login failed: {login_response.text}")

except Exception as e:
    print(f"Error: {e}")