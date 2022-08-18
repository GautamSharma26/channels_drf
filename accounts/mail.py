from django.core.mail import send_mail
from pizza.settings import EMAIL_HOST_USER


def mail_send(message, token, title):
    send_mail(
        # from here a token is sending to mail which is assigned to that user.
        # "Password Reset for {title}".format(title="Pizza app"),
        subject=title,
        # message:
        message=message,
        # from:
        # from_email="noreply@somehost.local",
        from_email=EMAIL_HOST_USER,
        # to:
        recipient_list=[token.user.email],
        # fail_silently=True
    )
