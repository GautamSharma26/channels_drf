from channels.generic.websocket import WebsocketConsumer
from .models import *
from asgiref.sync import async_to_sync
import json


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
        self.send(text_data=json.dumps({
            "payload": order
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
