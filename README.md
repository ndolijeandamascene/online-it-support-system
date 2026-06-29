# Online IT Support System

A Django and Django Templates based help desk application for managing IT support requests, internal communication, knowledge articles, assets, and reporting foundations.

## Overview

The Online IT Support System centralizes IT support operations for companies, schools, government institutions, and other organizations. Employees or clients can submit technical issues, IT staff can assign and resolve tickets, and administrators can monitor service activity from a single web interface.

## Objectives

- Digitize IT support requests.
- Improve communication between users and IT staff.
- Track every support request from submission to resolution.
- Provide dashboard and report foundations for decision-making.
- Support future PDF, Excel, email, and real-time notification features.

## Main users

- Administrator
- IT Support Staff
- Department Manager
- Employee or Client

## Features

- Dashboard with ticket status and priority statistics.
- Create support tickets with category, priority, requester, issue details, and file attachments.
- Search and filter tickets by status or keyword.
- View ticket details with requester metadata and status badges.
- Assign tickets to IT support staff.
- Update ticket status, priority, and resolution notes.
- Add public or internal support-team conversation notes.
- Knowledge base for FAQs, troubleshooting guides, and manuals.
- Asset-management data model for computers, devices, maintenance, and warranties.
- Notification and audit-log data models.
- Reports page with ticket totals by status, category, and department.
- Manage departments, profiles, tickets, assets, articles, notifications, and audit logs from Django admin.

## Technology stack

- Backend: Django
- Frontend: Django Templates, HTML5, CSS3
- Database: SQLite for development; PostgreSQL recommended for production
- Authentication: Django Authentication
- File storage: Django Media

## Quick start

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/` for the support desk and `http://127.0.0.1:8000/admin/` for administration.
