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
