from celery import shared_task
from django.core.mail import send_mail
from pizza.settings import EMAIL_HOST_USER


@shared_task
def mail_send(message, token, title):
    send_mail(
        # from here a token is sending to mail which is assigned to that user.
        subject=title,
        # message:
        message=message,
        # from:
        from_email=EMAIL_HOST_USER,
        # to:
        recipient_list=[token],
        # fail_silently=True
    )
