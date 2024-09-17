## Features
- User registration and login.
- Event creation, registration, and management.
- Email reminders for registered users about upcoming events.
- Background tasks handled by Celery (sending emails, reminders).
- Redis as the message broker for Celery tasks.
- Django Admin interface for managing events and users.

## Prerequisites
1. Set up the .env File
"touch .env"
2. Add the following environment variables to your .env file
"SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password"
3. Build and Run the Application with Docker
"docker-compose up --build"
4. Create a Superuser for Admin Access
"docker-compose exec django python manage.py createsuperuser"
User Interface: http://localhost:8000, http://127.0.0.1:8000
Admin Panel: http://localhost:8000/admin
Stop the running Docker containers
"docker-compose down"