# Event Manager

Django event management project with REST API, JWT authentication, Celery tasks, Redis broker, and Docker support.

## Features

- User registration and login
- Event CRUD and registration flow
- Reminder emails for event attendees
- Celery worker and periodic tasks
- Redis integration
- Django Admin panel

## Quick Start

1. Create environment file:

```bash
cp .env.example .env
```

2. Run with Docker:

```bash
docker-compose up --build
```

3. Create admin user:

```bash
docker-compose exec django python manage.py createsuperuser
```

## Local URLs

- App: `http://localhost:8000`
- Admin: `http://localhost:8000/admin`
- Swagger: `http://localhost:8000/swagger/`

## Stop containers

```bash
docker-compose down
```
