import json

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from .models import *
from .serializer import OrderSerializerSignal, StatusSerializerSignal, StatusLogSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@receiver(post_save, sender=CartPizza)
def total_amount_add(sender, instance, created, **kwargs):
    if created:
        cart = Cart.objects.get(user=instance.cart.user)
        cart.total_amount += instance.pizza.price * int(instance.quantity)
        cart.save()
        instance.total_amount += instance.pizza.price * int(instance.quantity)
        instance.save()


@receiver(pre_delete, sender=CartPizza)
def total_amount_exclude(instance, **kwargs):
    user = instance.cart.user
    cart = Cart.objects.get(user=user)
    cart.total_amount -= instance.pizza.price * instance.quantity
    cart.save()


@receiver(post_save, sender=Order)
def order_signal(sender, instance, created, **kwargs):
    if not created:
        channel_layer = get_channel_layer()
        # data = {}
        # data['order_idd'] = instance.order_idd
        # data['status'] = instance.status.status_level
        order = Order.order_details(instance.order_idd)
        logs = StatusLog.objects.filter(order_id=order['id'])
        log_data = StatusLogSerializer(logs, many=True)
        async_to_sync(channel_layer.group_send)(
            'order_%s' % instance.order_idd, {
                'type': 'order_status_view',
                'value': json.dumps(log_data.data)
            }
        )


# @receiver(post_save, sender=Order)
# def statuslog(sender, instance, created, **kwargs):
#     if created:
#         StatusLog.objects.get(order_id=instance.id)
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#
#         )



@receiver(post_save, sender=Order)
def order_delivery(sender, instance, created, **kwargs):
    if created:
        serializer = OrderSerializerSignal(instance)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "all_order",
            {
                "type": "order_create_message",
                "value": json.dumps([serializer.data])
            }
        )


@receiver(post_save, sender=Order)
def order_accepted_signal(sender, instance, created, **kwargs):
    if not created:
        serializer = OrderSerializerSignal(instance)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "all_order",
            {
                "type": "order_accepted",
                "value": json.dumps([serializer.data])
            }
        )


@receiver(post_save, sender=Order)
def owner_order_signal(sender, instance, created, **kwargs):
    print("not called")
    if created:
        print("called")
        serializer = OrderSerializerSignal(instance)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "owner_order",
            {
                "type": "owner_order_show",
                "value": json.dumps([serializer.data])
            }
        )


@receiver(post_save, sender=Order)
def statusorder(sender, instance, created, **kwargs):
    if not created:
        print(instance.status.id)
        data = {
            "order": instance.id,
            "status": instance.status.id
        }
        print(f"d {data}")
        serializer = StatusSerializerSignal(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()