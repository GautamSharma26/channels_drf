from django.db import models
from accounts.models import User
from django.core.validators import MinValueValidator


# Create your models here.
Pizza_size = (
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
)


class Pizza(models.Model):
    name = models.CharField(max_length=100, null=False)
    price = models.IntegerField(null=False)
    image = models.ImageField(upload_to='pizza_img', null=False)
    size = models.CharField(max_length=10, choices=Pizza_size, default='S')

    def __str__(self):
        return str(self.name)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_ordered = models.BooleanField(default=False)
    total_amount = models.IntegerField(default=0)

    def __str__(self):
        return self.user


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    price = models.IntegerField(null=False)

    def __str__(self):
        return f"{self.user} {self.pizza}"


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    area = models.CharField(max_length=150, null=False)
    landmark = models.CharField(max_length=100, null=False)
    city = models.CharField(max_length=50, null=False)
    pincode = models.IntegerField(validators=[MinValueValidator(6)])

    def __str__(self):
        return f"{self.user} {self.area}"


Status_Choice = (
    ('Order Received', 'Order Received'),
    ('Baking', 'Baking'),
    ('Baked', 'Baked'),
    ('Out for Delivery', 'Out for Delivery'),
    ('Delivered', 'Delivered'),
)


class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False)
    total_amount = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=Status_Choice, default='Order Received')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cart} Pizza Order"
