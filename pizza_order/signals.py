import json

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from .models import *
from celery import shared_task
from accounts.mail import mail_send
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@receiver(post_save, sender=CartPizza)
def total_amount_add(sender, instance, created, **kwargs):
    if created:
        cart = Cart.objects.get(user=instance.cart.user)
        cart.total_amount += instance.pizza.price * int(instance.quantity)
        cart.save()
        cart_pizza = CartPizza.objects.get(cart=cart, pizza=instance.pizza)
        cart_pizza.total_amount += instance.pizza.price * int(instance.quantity)
        cart_pizza.save()


@receiver(pre_delete, sender=CartPizza)
def total_amount_exclude(instance, **kwargs):
    user = instance.cart.user
    cart = Cart.objects.get(user=user)
    cart.total_amount -= instance.pizza.price * instance.quantity
    cart.save()


@shared_task
def send_mail_func(token):
    title = "Pizza Ordered"
    message = "Order done"
    # token = ['gautamkr1998@gmail.com'],
    mail_send(message, token, title)

    return "Done"


@receiver(post_save, sender=Order)
def order_signal(sender, instance, created, **kwargs):
    if not created:
        channel_layer = get_channel_layer()
        data = {}
        print(instance.order_idd)
        data['order_idd'] = instance.order_idd
        data['status'] = instance.status
        async_to_sync(channel_layer.group_send)(
            'order_%s' % instance.order_idd, {
                'type': 'order_status_view',
                'value': json.dumps(data)
            }
        )
