# Task Management Web Application

A Django-based web application for managing tasks and assignments, sharing the same PostgreSQL database with a Tkinter desktop application.

## Features

- User authentication (login, registration)
- Role-based access control (Admin/Assigner vs Regular User/Assignee)
- Task/Assignment management (Create, Read, Update, Delete)
- Status tracking for assignments
- Responsive web interface using Bootstrap 5

## Prerequisites

- Python 3.8 or higher
- PostgreSQL database
- Virtual environment (recommended)

## Setup Instructions

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your database credentials:
```
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432
```

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser (admin):
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

7. Access the application at http://127.0.0.1:8000/

## Project Structure

- `taskmanager/` - Main project directory
  - `tasks/` - Main application for task management
  - `templates/` - HTML templates
  - `static/` - Static files (CSS, JS, images)
  - `manage.py` - Django management script

## Database Schema

The application uses the following main models:
- User (Django's built-in User model)
- Assignment (Task/Assignment model with creator and assignees)

## Security

- CSRF protection enabled
- Password hashing via Django's auth system
- Role-based access control
- SQL injection protection via Django ORM 