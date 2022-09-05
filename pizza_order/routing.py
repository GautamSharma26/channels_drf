from django.urls import re_path
from .consumers import OrderStatus, OrderDelivered, ShopOwner

websocket_urlpatterns = [
    re_path(r'ws/order/(?P<order_idd>\w+)/$', OrderStatus.as_asgi()),
    re_path(r'ws/order/$', OrderDelivered.as_asgi()),
    re_path(r'ws/owner/(?P<current_user>\w+)/$', ShopOwner.as_asgi()),
]
