from channels.generic.websocket import WebsocketConsumer
from .models import *
from asgiref.sync import async_to_sync
import json
from .serializer import OrderSerializer, StatusLogSerializer


class OrderStatus(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['order_idd']
        self.room_group_name = "order_%s" % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        order = Order.order_details(self.room_name)
        logs = StatusLog.objects.filter(order_id = order['id'])
        log_data = StatusLogSerializer(logs,many=True)
        self.send(text_data=json.dumps({
            "payload": log_data.data
        }))

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'order_status_view',
                'payload': text_data
            }
        )

    def order_status_view(self, event):
        order = json.loads(event['value'])
        self.send(text_data=json.dumps({
            'payload': order
        })
        )


class OrderDelivered(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = None

    def connect(self):
        self.room_group_name = "all_order"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        order = Order.objects.filter(is_delivered="False")
        serializer = OrderSerializer(order, many=True)
        self.send(text_data=json.dumps({
            "payload": serializer.data
        }))

    # def disconnect(self, code):
    #     super(OrderDelivered, self).disconnect()

    def receive(self, text_data=None, bytes_data=None):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "order_create_message",
                "payload": text_data
            })
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "order_accepted",
                "payload": text_data
            }
        )

    def order_create_message(self, event):
        order = json.loads(event['value'])
        self.send(text_data=json.dumps({
            "payload": order
        }))

    def order_accepted(self, event):
        order = json.loads(event['value'])
        self.send(text_data=json.dumps({
            "payload": order
        }))


class ShopOwner(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['current_user']
        self.room_group_name = "owner_order"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        user = User.objects.get(id=self.room_name)
        shop_data = user.shop_set.all().filter(owner=user)
        if shop_data:
            for data in shop_data:
                order = Order.objects.filter(is_delivered="False", shop_id=data.id)
                serializer = OrderSerializer(order, many=True)
                self.send(text_data=json.dumps({
                    "payload": serializer.data
                }))
        else:
            self.send(text_data=json.dumps({
                "payload": "None"
            }))

    def disconnect(self, code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        print(f"text {text_data}")
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "owner_order_show",
                "payload": text_data
            }
        )

    def owner_order_show(self, event):
        order = json.loads(event["value"])
        self.send(text_data=json.dumps(
            {
                "payload": order
            }
        ))
