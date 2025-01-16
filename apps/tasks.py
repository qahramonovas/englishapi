from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from root import settings


@shared_task
def send_email_task(email, code):
    message = f"Code: {code}"
    send_mail(
        "Your verification code",
        message,
        settings.EMAIL_HOST_USER,
        [email],
    )
    return {"message": "success"}

