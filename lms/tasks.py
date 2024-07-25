import smtplib

from celery import shared_task
from django.core.mail import send_mail

from django.conf import settings

from config.settings import EMAIL_HOST_USER
from lms.models import Subscription, Course


@shared_task
def send_email(course_id):
    """Sends email to subscribers if a course hasn't been updated for more than 4 hours"""
    subscriptions = Subscription.objects.filter(course_id=course_id, status=True)
    emails = []
    if subscriptions:
        course_name = subscriptions[0].course.title
        for subscription in subscriptions:
            emails.append(subscription.user.email)

    if len(emails) > 0:
        try:
            send_mail(subject=f'Обновление курса {course_name}',
                      message=f'По вашей подписке {course_name} вышел новый урок!',
                      from_email=settings.EMAIL_HOST_USER,
                      recipient_list=emails)
        except smtplib.SMTPException as e:
            raise print(f"Ошибка отправки сообщения {e}")

@shared_task
def send_email(course_id):
    course = Course.objects.get(pk=course_id)

    subscriptions = Subscription.objects.filter(course=course, status=True)
    emails = list(subscriptions.values_list(user__email, flat=True))

    send_mail(
        subject=f'Обновление курса {course.title}',
        message=f'По вашей подписке {course.title} вышел новый урок!',
        from_email=EMAIL_HOST_USER,
        recipient_list=emails
    )
