from django.urls import path
from .views import *

urlpatterns = [
    path('', PizzaAdminView.as_view({'get': 'list', 'post': 'create'})),
    path('product_view/<int:pk>', PizzaAdminView.as_view({'delete': 'destroy', 'patch': 'partial_update'})),
    path('view_product/', PizzaAllView.as_view({'get': 'list'})),
    path('address/', AddressView.as_view({'get': 'list'})),
    path('address_write/<int:pk>', AddressView.as_view({'delete': 'destroy', 'patch': 'partial_update'})),
    path('address_create/', AddressCreate.as_view({'post': 'create'})),
]
