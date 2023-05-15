from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class CategorySerializer(serializers.Serializer):
    class Meta:
        model = Categories
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.productName = validated_data.get('productName', instance.productName)
        instance.productCategory = validated_data.get('productCategory', instance.productCategory)
        instance.productImage = validated_data.get('productImage', instance.productImage)
        instance.productPrice = validated_data.get('productPrice', instance.productPrice)
        instance.productDescription = validated_data.get('productDescription', instance.productDescription)
        instance.save()
        return instance
