from django.template.backends import django
from django.urls import path, include
from .views import *
from pizza import settings

urlpatterns = [
    path('', PizzaAdminView.as_view({'get': 'list', 'post': 'create'})),
    path('product_view/<int:pk>', PizzaAdminView.as_view({'delete': 'destroy', 'patch': 'partial_update'})),
    path('view_product/', PizzaAllView.as_view({'get': 'list'})),
    path('address/', AddressView.as_view({'get': 'list'})),
    path('address_write/<int:pk>', AddressWrite.as_view({'delete': 'destroy', 'patch': 'partial_update'})),
    path('address_create/', AddressCreate.as_view({'post': 'create'})),
    path('cart/', CartView.as_view({'post': 'create', 'get': 'list'})),
    path('cartpizza/<int:pk>', CartPizzaView.as_view({'patch': 'partial_update', 'delete': 'destroy'})),
    path('cartpizza/', CartPizzaView.as_view({'get': 'list'})),
    path('order/', OrderCreate.as_view({'post': 'create', 'get': 'list'})),
    path('login/', login_request, name='login'),
    path('home/order_status/<str:order_idd>', order_status, name='order_status'),
    path('home/', home, name='home'),
    path('success/', success_payment),
    path('cancel/', cancel_payment),
    path('webhook/', stripe_webhook),
    path('order_delivered/', order_delivered, name="order_delivered"),
    path('order_delivered_url/<int:id>/<int:data>/', order_delivered_url, name="order_delivered_url"),
    path('shop/', ShopCreate.as_view({'post': 'create', 'get': 'list'}), name="shop"),
    path('shop/<int:pk>/', ShopCreate.as_view({'patch': 'partial_update', 'delete': 'destroy'}), name="shop"),
    path('shop-owner/', shop_owner, name='shop_owner')
]
