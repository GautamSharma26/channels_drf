from celery import shared_task
from django.core.mail import send_mail
from pizza.settings import EMAIL_HOST_USER
from pizza_order.models import Order, Status
# from pizza_order.serializer import StatusSerializerSignal, Scheduled_Serializer
# from .stripe_utils import stripe_session_create, stripe_customer_create
# from .permission import IsOwner


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


@shared_task
def add(order_data):
    data_order = Order.objects.filter(id=order_data).first()
    obj_status = Status.objects.get(id=1)
    if data_order:
        data_order.status = obj_status
        data_order.save()


@shared_task(name='did')
def did():
    return "a"