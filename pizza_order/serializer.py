from rest_framework import serializers
from .models import *


class PizzaSerializer(serializers.ModelSerializer):
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

    class Meta:
        model = Cart
        fields = '__all__'


class CartPizzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartPizza
        fields = ['id', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.CharField(default=serializers.CurrentUserDefault())
    total_amount = serializers.IntegerField()

    class Meta:
        model = Order
        fields = '__all__'

class OrderSerializerSignal(serializers.ModelSerializer):
    user = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = "__all__"

class DeliveryBoySerializer(serializers.ModelSerializer):
    delivery_boy = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = DeliveryBoy
        fields = "__all__"

