from channels.generic.websocket import WebsocketConsumer
from .models import *
from asgiref.sync import async_to_sync
import json
from .serializer import OrderSerializer, StatusLogSerializer, OrderSerializerSignal
import googlemaps
from pizza import settings


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
        logs = StatusLog.objects.filter(order_id=order['id'])
        log_data = StatusLogSerializer(logs, many=True)
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
        self.user_data = None
        self.room_group_name = None

    def connect(self):
        self.user_data = self.scope['url_route']['kwargs']['current_user']
        self.room_group_name = "all_order"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        # data_user = User.objects.filter(id=self.user_data).first()
        User.objects.prefetch_related('address_set').filter(id=self.user_data)
        status_obj = Status.objects.get(status_level="Ready For Delivery")
        gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)
        now = datetime.datetime.now()
        order = Order.objects.filter(is_delivered="False", status=status_obj.id)
        if order:
            # serializer = OrderSerializer(order, many=True)
            # self.send(text_data=json.dumps({
            #     "payload": serializer.data, "map_data": str(gmaps)
            # }))
            for data_order in order:
                print(data_order,"data")
                calculate = json.dumps(gmaps.distance_matrix("Shivranjani Ahmedabad",
                                                             data_order.address.area + "," + data_order.address.city,
                                                             mode="driving", departure_time=now))
                calculate2 = json.loads(calculate)
                distance = calculate2['rows'][0]['elements'][0]['distance']['text']
                print(distance, "main")
                if distance < str(10):
                    data = {}
                    data['id']=data_order.id
                    data['status'] = str(data_order.status)
                    data['user'] = str(data_order.user)
                    self.send(text_data=json.dumps({
                        "payload":[data] , "map_data": str(gmaps)
                    }))
        # if order:
        #     for data_order in order:
        #         calculate = json.dumps(gmaps.distance_matrix("Shivranjani Ahmedabad",
        #                                                      data_order.address.area + "," + data_order.address.city,
        #                                                      mode="driving",
        #                                                      departure_time=now))
        #         calculate2 = json.loads(calculate)
        #         distance = calculate2['rows'][0]['elements'][0]['distance']['text']
        #         print(distance, "main")
        #         if distance < str(10):
        #             serializer = OrderSerializer(order, many=True)
        #             self.send(text_data=json.dumps({
        #                 "payload": serializer.data, "map_data": str(gmaps)
        #             }))
        else:
            self.send(text_data=json.dumps({
                "payload": "None"
            }))

    # def disconnect(self, code):
    #     super(OrderDelivered, self).disconnect()

    def receive(self, text_data=None, bytes_data=None):
        print("text")
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "order_create_message",
                "payload": text_data
            })
        # async_to_sync(self.channel_layer.group_send)(
        #     self.room_group_name,
        #     {
        #         "type": "order_accepted",
        #         "payload": text_data
        #     }
        # )

    def order_create_message(self, event):
        order = json.loads(event['value'])
        print("order", order[0]['address'])
        data_order = order[0]['address']
        gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)
        now = datetime.datetime.now()
        address_data = Address.objects.get(id=data_order)

        calculate = json.dumps(
            gmaps.distance_matrix("Shivranjani Ahmedabad", address_data.area + "," + address_data.city,
                                  mode="driving",
                                  departure_time=now))
        calculate2 = json.loads(calculate)
        distance = calculate2['rows'][0]['elements'][0]['distance']['text']
        print(distance, "signal")
        if distance < str(10):
            # serializer = OrderSerializer(order, many=True)
            self.send(text_data=json.dumps({
                "payload": order,
            }))
        else:
            self.send(text_data=json.dumps({
                "payload": "None"
            }))

    # def order_accepted(self, event):
    #     order = json.loads(event['value'])
    #     self.send(text_data=json.dumps({
    #         "payload": order
    #     }))


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
                status_obj = Status.objects.get(status_level="Order Received")
                order = Order.objects.filter(is_delivered="False", shop_id=data.id, status_id=status_obj.id)
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
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "owner_order_show",
                "payload": text_data
            }
        )

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "owner_order_changes",
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

    def owner_order_changes(self, event):
        order = json.loads(event["value"])
        self.send(text_data=json.dumps(
            {
                "payload": order
            }
        ))
