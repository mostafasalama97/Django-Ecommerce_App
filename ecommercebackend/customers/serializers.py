from rest_framework import serializers

from product.serializers import ProductSerializer
from .models import *
from django.contrib.auth.models import User


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


    # def update(self, instance, validated_data):
    #     orders_data = validated_data.pop('orders', [])
    #     orders_serializer = OrderSerializer(instance=instance.orders.all(), data=orders_data, many=True)
    #     if orders_serializer.is_valid():
    #         orders_serializer.save()

    #     return super().update(instance, validated_data)

class CustomerWishListSerializer(serializers.ModelSerializer):
    wish_list = ProductSerializer(many=True)

    class Meta:
        model = Customer
        fields = ['customer_ID', 'customer_name', 'customer_phone_number', 'customer_address', 'wish_list']



class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderProduct
        fields = ['id', 'product', 'quantity']


