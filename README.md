# AcademiaOS — Academic ERP System

[![Project Status: Completed](https://img.shields.io/badge/Project%20Status-Completed-success.svg)](#)
[![Backend: Django](https://img.shields.io/badge/Backend-Django%206.0%20%2F%20DRF-green.svg)](#)
[![Frontend: React](https://img.shields.io/badge/Frontend-React%2019%20%2F%20Vite%208-blue.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](#)

AcademiaOS is a comprehensive, production-ready Academic Enterprise Resource Planning (ERP) system designed to streamline and automate academic operations for educational institutions. With role-based portals for administrators, faculty members, and students, the application manages multi-tenant registrations, course schedules, batch-wise attendance, grade inputs, and academic structures.

---

## 📖 Table of Contents

1. [Key Features](#-key-features)
2. [Tech Stack & Architecture](#-tech-stack--architecture)
3. [Project Directory Structure](#-project-directory-structure)
4. [Getting Started & Installation](#-getting-started--installation)
   - [Prerequisites](#prerequisites)
   - [Backend Setup](#backend-setup)
   - [Frontend Setup](#frontend-setup)
5. [Demo & Testing Credentials](#-demo--testing-credentials)
6. [Useful Management Commands](#-useful-management-commands)
7. [API Endpoints & Swagger Documentation](#-api-endpoints--swagger-documentation)
8. [Troubleshooting & Visibility Resolutions](#-troubleshooting--visibility-resolutions)
9. [Verification & System Testing](#-verification--system-testing)

---

## 🌟 Key Features

### 1. Dynamic Multi-Tenant Registration System
*   **Custom Fields Management**: Administrators can define custom registration fields (e.g., text, numbers, dates, dropdowns, email, phone) on a per-institution/tenant basis.
*   **Flexible Storage**: Fields are saved inside a JSONField in the student's profile, validating inputs dynamically both on the client and server side.
*   **Program-Based Structure**: Degree programs are dynamically tied to academic departments with credit management limits.

### 2. Streamlined Semester Registration Workflow
*   **Auto-Assignment**: Automated core course enrollment for first-semester students.
*   **Backlog & Prerequisite Verification**: Automatic checking for course pre-requisites and credit thresholds.
*   **Fee Integration**: Integrates tracking for registration fees with support for multi-step transaction history.
*   **Admin Approval Dashboard**: Unified approval interface for pending student registration requests.

### 3. Batch-Wise Attendance System
*   **Bulk Attendance Marking**: Allows faculty members to mark attendance for an entire class in a single request.
*   **Roll Number Pattern Recognition**: Automatic grouping and sorting of student registrations based on roll numbers.
*   **Conflict Prevention**: Unique DB constraints ensure no double marking occurs for a student, subject, and date.
*   **Attendance Submission**: Workflow for faculty to submit reports for admin review.

### 4. Faculty-Guided Grading System
*   **Faculty Autonomy**: Manual entry of marks and letter grades on a 10-point scale (A=10.0 to F=0.0). No automatic calculations are forced, ensuring academic freedom.
*   **CGPA/GPA Calculations**: Automatically recalculates cumulative performance from finalized grades.
*   **Detailed Analytics**: Subject-wise analytics, pass/fail ratios, and class-wide performance distributions.

### 5. Timetable Conflict-Detection & Management
*   **PDF Schedule Uploads**: Admins can upload timetables as PDFs for specific departments or institution-wide.
*   **Role-Based Visibility**: Students and faculty are shown only timetables relevant to their department or those marked as institution-wide.
*   **Schedule Conflict Alerts**: Backend conflict validation prevents overlapping class assignments.

---

## 🛠 Tech Stack & Architecture

### Backend Infrastructure
*   **Framework**: [Django 6.0.2](https://www.djangoproject.com/) & [Django REST Framework 3.16.1](https://www.django-rest-framework.org/)
*   **Database**: SQLite (for development), PostgreSQL (for production/deployment)
*   **Authentication**: JWT (JSON Web Tokens) via `djangorestframework-simplejwt`
*   **API Docs**: Swagger / OpenAPI using `drf-yasg`
*   **Testing**: Django test suite & Property-Based Testing using `Hypothesis`

### Frontend Infrastructure
*   **Framework**: [React 19.2.4](https://react.dev/) & [Vite 8.0.1](https://vite.dev/)
*   **Routing**: React Router DOM (v7)
*   **HTTP Client**: Axios with interceptors for token refresh
*   **Styling**: Modular CSS3 with clean, responsive grid/flex layouts

```
┌──────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│  React Frontend  │      │  Django Backend │      │   PostgreSQL    │
│  • Role routing  │ ◄──► │  • REST API     │ ◄──► │    Database     │
│  • Responsive UI │      │  • JWT Auth     │      │  • ACID Compliance│
└──────────────────┘      └─────────────────┘      └─────────────────┘
```

---

## 📁 Project Directory Structure

```
academia-os/
├── backend/
│   ├── apps/                 # Modular Django apps
│   │   ├── academics/        # Departments, courses, subjects, timetables
│   │   ├── assignments/      # Assignment tasks (read-only/archived)
│   │   ├── attendance/       # Bulk attendance, reports
│   │   ├── common/           # Shared models & helper classes
│   │   ├── communication/    # Noticeboards, alerts
│   │   ├── exams/            # Grading and exam schedules
│   │   ├── faculty/          # Faculty profiles, subjects assigned
│   │   ├── students/         # Student profiles, enrollments, registrations
│   │   └── users/            # Custom User models, role definitions, JWT Auth
│   ├── config/               # Settings, middleware, central URLs
│   ├── faculty_data.csv      # Import template data
│   ├── manage.py             # Django execution CLI
│   └── requirements.txt      # Backend dependencies
│
├── frontend/
│   ├── public/               # Public assets
│   ├── src/
│   │   ├── components/       # Layouts, Login, Toast, Modals, Route protections
│   │   ├── pages/            # Role dashboards (Admin, Faculty, Student)
│   │   ├── api.js            # Central API endpoints client with Axios
│   │   └── App.jsx           # Routing configuration
│   ├── package.json          # Node dependencies & scripts
│   └── vite.config.js        # Vite configurations
│
├── PROJECT_REPORT.md         # Detailed development status
└── TIMETABLE_ISSUE_RESOLUTION.md  # Troubleshooting guidelines
```

---

## 🚀 Getting Started & Installation

### Prerequisites
*   Python 3.10+
*   Node.js 18+ (with npm)

### Backend Setup

1.  **Navigate to the backend directory**:
    ```bash
    cd backend
    ```

2.  **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    
    # On Windows (PowerShell):
    .\venv\Scripts\Activate.ps1
    
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create your environment configuration**:
    Create a `.env` file based on `.env.example`:
    ```bash
    cp .env.example .env
    ```
    *(Adjust database, secret keys, or debug settings in `.env` as required).*

5.  **Run migrations and apply database schema**:
    ```bash
    python manage.py migrate
    ```

6.  **Seed mock data for development**:
    ```bash
    python manage.py seed_data
    ```

7.  **Start the local Django server**:
    ```bash
    python manage.py runserver
    ```
    *(The backend API will run on [http://127.0.0.1:8000](http://127.0.0.1:8000))*

---

### Frontend Setup

1.  **Navigate to the frontend directory**:
    ```bash
    cd ../frontend
    ```

2.  **Install frontend packages**:
    ```bash
    npm install
    ```

3.  **Run the local Vite development server**:
    ```bash
    npm run dev
    ```
    *(The web interface will run on [http://localhost:5173](http://localhost:5173) or [http://localhost:5174](http://localhost:5174))*

---

## 🔑 Demo & Testing Credentials

Use the following pre-seeded credentials to log in and inspect individual portals:

| Role | Username | Password | Notes |
| :--- | :--- | :--- | :--- |
| **System Administrator** | `admin_demo` | `Admin@2026` | Full system control, user setup |
| **Faculty Member** | `prof_smith` | `Faculty@2026` | Attendance and grades marking |
| **Student** | `john_doe` | `Student@2026` | Enrollment, timetable view, results |

### Special Timetable Validation Accounts
For testing the role-restricted department timetable logic:
*   **Student** (CSE Dept): `Aksh` / `Student@2026` (Should see global timetables only)
*   **Faculty** (ES Dept): `aj_k` / `Faculty@2026` (Should see ES and global timetables)

---

## 🛠 Useful Management Commands

AcademiaOS features custom Django administrative commands to speed up development:

*   **Synchronize Programs**: Connect course requirements with program parameters.
    ```bash
    python manage.py sync_programs
    ```
*   **Seed Real Academic Content**: Populates real departments, courses, and schedules.
    ```bash
    python manage.py seed_real_data
    ```
*   **Import Faculty from CSV**: Import profiles directly.
    ```bash
    python manage.py import_faculty faculty_data.csv
    ```
*   **Safe Hard/Soft Deletion**:
    ```bash
    python manage.py delete_courses --codes BTECH-CSE
    python manage.py simple_delete_depts --codes MATH CS
    ```

For a full list of shell tricks and custom admin capabilities, refer to [MANAGEMENT_COMMANDS.md](file:///c:/NVJKA/NVJKA/NVJKA/backend/MANAGEMENT_COMMANDS.md).

---

## 📌 API Endpoints & Swagger Documentation

When running the backend server locally, detailed documentation of all REST controllers is accessible at:
*   **Interactive Swagger UI**: [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)
*   **ReDoc UI**: [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)

### Key API Layout:
*   `POST /api/auth/login/` — Token generation (JWT access + refresh)
*   `GET/POST /api/academics/custom-fields/` — Multi-tenant registration field configurations
*   `POST /api/students/semester-register/` — Registration requests
*   `POST /api/attendance/bulk-mark/` — Faculty batch marking
*   `POST /api/faculty/grades/` — Grade assignments

---

## 🔍 Troubleshooting & Visibility Resolutions

If data (such as Timetables or Student Attendance) is not displaying in the frontend, ensure the following setup steps:
1.  **CORS Allowed Origins**: Ensure `backend/config/settings.py` includes the active Vite dev port in the `CORS_ALLOWED_ORIGINS` list.
2.  **API Base URL**: Confirm `frontend/src/api.js` connects to the correct protocol and port (default is `http://127.0.0.1:8000`).
3.  **Local Storage Cache**: If switching roles on the same browser window, clear local storage or open an Incognito page to purge conflicting cookies or user credentials.

For deep-dive steps, view the [TIMETABLE_ISSUE_RESOLUTION.md](file:///c:/NVJKA/NVJKA/NVJKA/TIMETABLE_ISSUE_RESOLUTION.md) file.

---

## 🧪 Verification & System Testing

To execute automated tests inside the backend:
```bash
cd backend
python manage.py test
```
To run tests specifically on selected apps:
```bash
python manage.py test apps.academics
python manage.py test apps.users
python manage.py test apps.attendance
```
