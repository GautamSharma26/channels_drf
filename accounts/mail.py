from django.core.mail import send_mail


def mail_send(email_plaintext_message, reset_password_token):
    send_mail(
        # from here a token is sending to mail which is assigned to that user.
        # title:
        "Password Reset for {title}".format(title="Pizza Delivery"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )