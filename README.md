# UI DLC Student Attendance Tracking System
Academic prototype for a University of Ibadan Distance Learning Centre case study. Not an official University of Ibadan service.

## Features
- Django authentication for lecturer/admin staff
- Student and course management through Django admin
- Assign enrolled students to courses
- Create attendance sessions and mark present/absent
- Prevent duplicate records per student per session
- View attendance rates and export CSV
- Staff access restrictions for courses

## Run locally (Python 3.10+)
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations tracker
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Visit http://127.0.0.1:8000/admin/ to add students, lecturer users, courses, and enrollments. Assign each course to a lecturer user. Then visit http://127.0.0.1:8000/ to sign in and record attendance.

## Tests
```bash
python manage.py test
```

## GitHub upload
Create an empty GitHub repository in your own account, then run:
```bash
git init
git add .
git commit -m "Initial UI DLC attendance tracking system"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```
Replace placeholders with your repository details. Do not commit student personal data, .env, or SQLite databases.

## Limitations
This MVP uses staff-recorded attendance; it does not implement QR codes, biometric verification, student self-service login, or integration with University of Ibadan systems. SQLite and development settings are not suitable for production deployment without hardening.
