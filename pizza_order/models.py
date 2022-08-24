import random
import string

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
        return f"{self.user} {self.area}"


Pizza_size = (
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
)


class Pizza(models.Model):
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
    quantity = models.IntegerField(null=False)
    total_amount = models.IntegerField(default=0)

    def __str__(self):
        return str(self.pizza)


def random_string_generator(size=10, chars=string.ascii_lowercase+string.digits):
    return ''.join(random.choice(chars)for _ in range(size))


Status_Choice = (
    ('Order Received', 'Order Received'),
    ('Baking', 'Baking'),
    ('Baked', 'Baked'),
    ('Out for Delivery', 'Out for Delivery'),
    ('Delivered', 'Delivered'),
)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pizza = models.ManyToManyField(Pizza, through="OrderPizza")
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=False)
    order_idd = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=Status_Choice, default='Order Received')
    date = models.DateTimeField(auto_now_add=True)
    total_amount = models.IntegerField(default=0)
    is_payed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.address} Pizza Order"

    def save(self, *args, **kwargs):
        if not len(self.order_idd):
            self.order_idd = random_string_generator()
        super(Order, self).save(*args, **kwargs)

    @staticmethod
    def order_details(order_idd):
        instance = Order.objects.filter(order_idd=order_idd).first()
        data={}
        data['order_idd'] = instance.order_idd
        data['status'] = instance.status

        return data


class OrderPizza(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(null=False)
    total_amount = models.IntegerField(default=0)

    def __str__(self):
        return str(self.pizza.name)
