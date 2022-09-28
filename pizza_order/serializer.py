from rest_framework import serializers
from .models import *


class PizzaSerializer(serializers.ModelSerializer):
    # shop = serializers.CharField()

    class Meta:
        model = Pizza
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.CharField()

    class Meta:
        model = Address
        fields = '__all__'


class AddressWriteSerializer(serializers.ModelSerializer):
    user = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Address
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    pizza = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")

    # shop = serializers.CharField()

    class Meta:
        model = Cart
        fields = '__all__'


class CartPizzaSerializer(serializers.ModelSerializer):
    shop = serializers.CharField()

    class Meta:
        model = CartPizza
        fields = ['id', 'quantity', 'shop']


class OrderSerializer(serializers.ModelSerializer):
    pizza = PizzaSerializer(many=True, read_only=True)
    user = serializers.CharField(default=serializers.CurrentUserDefault())
    total_amount = serializers.IntegerField()
    # status = serializers.CharField()

    class Meta:
        model = Order
        fields = '__all__'

class OrderSerializerView(serializers.ModelSerializer):
    pizza = PizzaSerializer(many=True, read_only=True)
    user = serializers.CharField(default=serializers.CurrentUserDefault())
    total_amount = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)
    address = serializers.CharField(read_only=True)
    shop = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class OrderSerializerSignal(serializers.ModelSerializer):
    pizza = PizzaSerializer(many=True, read_only=True)
    # address = serializers.CharField()
    user = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = "__all__"


class DeliveryBoySerializer(serializers.ModelSerializer):
    delivery_boy = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = DeliveryBoy
        fields = "__all__"


class ShopSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Shop
        fields = '__all__'

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"


class StatusLogSerializer(serializers.ModelSerializer):
    # order = serializers.CharField(read_only=True)
    status = StatusSerializer()
    class Meta:
        model = StatusLog
        fields = "__all__"

class StatusSerializerSignal(serializers.ModelSerializer):
    class Meta:
        model = StatusLog
        fields = "__all__"


# class Scheduling_Serializer(serializers.ModelSerializer):
#     # user = serializers.CharField(default=serializers.CurrentUserDefault())
#     class Meta:
#         model = Scheduling_Order
#         fields = "__all__"

class Scheduled_Serializer(serializers.ModelSerializer):
    # user = serializers.CharField()
    date = serializers.DateTimeField()
    # id = serializers.IntegerField(read_only=True)
    # total_amount = serializers.IntegerField()

    class Meta:
        model = Order
        fields = "__all__"

