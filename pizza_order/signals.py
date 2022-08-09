from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import *
from celery import shared_task
from django.core.mail import send_mail
from pizza.settings import EMAIL_HOST_USER


@receiver(post_save, sender=Cart)
def total_amount_add(instance, created, **kwargs):
    if created:
        cart = Cart.objects.get(user=instance.user, is_ordered=False)
        cart.total_amount += instance.price * instance.quantity
        cart.save()


@shared_task
def send_mail_func():
    send_mail(
        subject="Pizza Ordered",
        message="",
        from_email=EMAIL_HOST_USER,
        recipient_list=['gautamkr1998@gmail.com'],
        fail_silently=True,
    )
    return "Done"
