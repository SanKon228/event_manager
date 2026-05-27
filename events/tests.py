from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from .models import Attendee, Event
from .tasks import send_event_reminder


class EventModelTests(TestCase):
    def test_event_str_returns_title(self):
        organizer = User.objects.create_user(username="owner", password="pass1234")
        event = Event.objects.create(
            title="Security Meetup",
            description="Meetup",
            date=timezone.now().date() + timedelta(days=1),
            location="Kyiv",
            organizer=organizer,
        )
        self.assertEqual(str(event), "Security Meetup")


class EventApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="tester",
            password="pass1234",
            email="tester@example.com",
        )

    def test_registration_api_creates_user(self):
        payload = {
            "username": "new_user",
            "password": "strong-pass-123",
            "email": "new_user@example.com",
        }
        response = self.client.post("/api/register/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="new_user").exists())

    def test_events_endpoint_requires_auth(self):
        response = self.client.get("/api/events/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_create_event(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            "title": "Blue Team Briefing",
            "description": "Internal session",
            "date": (timezone.now().date() + timedelta(days=2)).isoformat(),
            "location": "Remote",
            "organizer": self.user.id,
        }
        response = self.client.post("/api/events/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Event.objects.filter(title="Blue Team Briefing").exists())

    def test_attendee_registration_is_unique_per_user_event(self):
        event = Event.objects.create(
            title="Threat Intel Sync",
            description="Review",
            date=timezone.now().date() + timedelta(days=1),
            location="Kyiv",
            organizer=self.user,
        )
        self.client.force_authenticate(user=self.user)
        first = self.client.post(f"/api/events/{event.id}/register/")
        second = self.client.post(f"/api/events/{event.id}/register/")
        self.assertEqual(first.status_code, status.HTTP_201_CREATED)
        self.assertEqual(second.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Attendee.objects.filter(event=event, user=self.user).count(), 1)


class ReminderTaskTests(TestCase):
    @patch("events.tasks.send_mail")
    def test_send_event_reminder_sends_email_for_today_event(self, mock_send_mail):
        organizer = User.objects.create_user(username="owner2", password="pass1234")
        attendee_user = User.objects.create_user(
            username="attendee1",
            password="pass1234",
            email="attendee1@example.com",
        )
        event = Event.objects.create(
            title="Morning Standup",
            description="Daily",
            date=timezone.now().date(),
            location="Online",
            organizer=organizer,
        )
        Attendee.objects.create(user=attendee_user, event=event)
        send_event_reminder()
        self.assertTrue(mock_send_mail.called)
