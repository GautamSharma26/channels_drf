import datetime
import random
import string
from django.utils import timezone
from django.db import models
from accounts.models import User
from django.core.validators import MinValueValidator


# Create your models here.


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    area = models.CharField(max_length=150, null=False)
    landmark = models.CharField(max_length=100, null=False)
    city = models.CharField(max_length=50, null=False)
    pincode = models.IntegerField(validators=[MinValueValidator(6)])

    def __str__(self):
        return self.area


class Shop(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=False)
    location = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name


Pizza_size = (
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
)


class Pizza(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False)
    price = models.IntegerField(null=False)
    image = models.ImageField(upload_to='pizza_img', null=False)
    is_deleted = models.BooleanField(default=False)
    size = models.CharField(max_length=10, choices=Pizza_size, default='S')

    def __str__(self):
        return str(self.name)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pizza = models.ManyToManyField(Pizza, through="CartPizza")
    total_amount = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user)


class CartPizza(models.Model):
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False)
    total_amount = models.IntegerField(default=0)

    def __str__(self):
        return str(self.pizza)


def random_string_generator(size=10, chars=string.ascii_lowercase+string.digits):
    return ''.join(random.choice(chars)for _ in range(size))


# Status_Choice = (
#     ('Order Received', 'Order Received'),
#     ('Baking', 'Baking'),
#     ('Baked', 'Baked'),
#     ('Out for Delivery', 'Out for Delivery'),
#     ('Delivered', 'Delivered'),
# )

class Status(models.Model):
    status_level = models.CharField(max_length=50,null=False)

    def __str__(self):
        return self.status_level


def get_default_status():
    status_level, _ = Status.objects.get_or_create(status_level="Order Received")
    return status_level


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pizza = models.ManyToManyField(Pizza, through="OrderPizza")
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=False)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, default=get_default_status)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    order_idd = models.CharField(max_length=100, blank=True)
    date = models.DateTimeField(default=timezone.now())
    total_amount = models.IntegerField(default=0)
    is_payed = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.address} Pizza Order"

    def save(self, *args, **kwargs):
        if not self.order_idd:
            self.order_idd = random_string_generator()
        super(Order, self).save(*args, **kwargs)

    @staticmethod
    def order_details(order_idd):
        instance = Order.objects.filter(order_idd=order_idd).first()
        data = {}
        data['id'] = instance.id
        data['order_idd'] = instance.order_idd
        data['status'] = instance.status.status_level

        return data


class OrderPizza(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(null=False)
    total_amount = models.IntegerField(default=0)

    def __str__(self):
        return str(self.pizza.name)


class DeliveryBoy(models.Model):
    delivery_boy = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return self.delivery_boy.first_name


class StatusLog(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.status


# class Scheduling_Order(models.Model):
#     order = models.IntegerField(null=True)
#     task = models.CharField(max_length=150, null=True)


# class Scheduled_Order(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     # pizza = models.ManyToManyField(Pizza, through="OrderPizza")
#     address = models.ForeignKey(Address, on_delete=models.CASCADE, null=False)
#     status = models.ForeignKey(Status, on_delete=models.CASCADE, default=get_default_status)
#     shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
#     order_idd = models.CharField(max_length=100, blank=True)
#     date = models.DateTimeField(null=False)
#     total_amount = models.IntegerField(default=0)
#     is_payed = models.BooleanField(default=False)
#     is_delivered = models.BooleanField(default=False)
#
#     def save(self, *args, **kwargs):
#         if not self.order_idd:
#             self.order_idd = random_string_generator()
#         super(Scheduled_Order, self).save(*args, **kwargs)
#
#


class Order_Scheduled_detail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    task = models.CharField(max_length=150)
