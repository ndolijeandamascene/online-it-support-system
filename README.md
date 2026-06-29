# Online IT Support System

A Django and Django templates based help desk application for managing IT support tickets.

## Features

- Create support tickets with category, priority, requester, and issue details.
- Search and filter tickets by status or keyword.
- View ticket details with requester metadata and status badges.
- Update ticket status and priority.
- Add support-team conversation notes.
- Manage tickets and updates from the Django admin.

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
