from django.urls import re_path

from .consumers import OrderStatus

websocket_urlpatterns = [
    re_path(r'ws/order/(?P<order_idd>\w+)/$', OrderStatus.as_asgi()),
]
