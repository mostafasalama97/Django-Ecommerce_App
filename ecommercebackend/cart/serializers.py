# serializers.py

from rest_framework import serializers

from product.serializers import ProductSerializer
from .models import *



class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    
    class Meta:
        model = CartItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, required=False)

    class Meta:
        model = Cart
        fields = '__all__'

class CartOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartOrder
        fields = '__all__'