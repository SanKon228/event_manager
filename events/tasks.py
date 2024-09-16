import logging
from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import Event, Attendee
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)

@shared_task
def send_event_reminder():
    try:
        today = timezone.now().date()
        events_today = Event.objects.filter(date=today)

        if not events_today.exists():
            logger.info("Подій на сьогодні не знайдено.")
            return

        for event in events_today:
            attendees = Attendee.objects.filter(event=event)

            if not attendees.exists():
                logger.info(f"У події '{event.title}' немає учасників.")
                continue

            for attendee in attendees:
                try:
                    send_mail(
                        'Нагадування про подію!',
                        f'Привіт {attendee.user.username}, сьогодні відбудеться подія "{event.title}". Не пропустіть!',
                        'noreply@example.com',
                        [attendee.user.email],
                        fail_silently=False,
                    )
                    logger.info(f"Нагадування відправлено {attendee.user.email} для події '{event.title}'")
                except Exception as e:
                    logger.error(f"Помилка при відправленні нагадування {attendee.user.email}: {str(e)}")
    except Exception as e:
        logger.error(f"Помилка під час виконання завдання send_event_reminder: {str(e)}")


@shared_task
def send_registration_email(event_title, user_email):
    try:
        logger.info(f"Початок завдання send_registration_email для події: {event_title} та користувача: {user_email}")

        send_mail(
            'Ви зареєструвалися на подію!',
            f'Ви успішно зареєструвалися на подію "{event_title}"',
            'noreply@example.com',
            [user_email],
            fail_silently=False,
        )

        logger.info(f"Лист реєстрації успішно відправлено на {user_email}")
    except Exception as e:
        logger.error(f"Помилка при відправленні листа реєстрації для {user_email}: {str(e)}")
