from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Pizza)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(Address)
admin.site.register(CartPizza)
admin.site.register(OrderPizza)
admin.site.register(DeliveryBoy)
admin.site.register(Shop)
admin.site.register(Status)
admin.site.register(StatusLog)
