from django.http import Http404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from product.models import Products
from .models import *
from .serializers import *

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import CartSerializer

class CartAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartSerializer
    queryset = Cart.objects.all()

    def post(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    def put(self, request, product_id=None, cart_item_id=None):
        cart, created = Cart.objects.get_or_create(user=request.user)
        try:
            product = get_object_or_404(Products, id=product_id)
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if cart_item_id:
            cart_item = get_object_or_404(CartItem, id=cart_item_id)
            if cart_item.cart.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            cart_item.delete()
        else:
            cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not item_created:
                cart_item.quantity += 1
                cart_item.save()
        serializer = self.get_serializer(cart)
        return Response(serializer.data)



    def delete(self, request, cart_item_id=None):
        cart_item = get_object_or_404(CartItem, id=cart_item_id)
        if cart_item.cart.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        cart_item.delete()
        serializer = self.get_serializer(cart_item.cart)
        return Response(serializer.data)

    def patch(self, request, cart_item_id=None):
        cart_item = get_object_or_404(CartItem, id=cart_item_id)
        if cart_item.cart.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        quantity = request.data.get('quantity', 1)
        if quantity < 1:
            cart_item.delete()
        else:
            cart_item.quantity = quantity
            cart_item.save()
        serializer = self.get_serializer(cart_item.cart)
        return Response(serializer.data)

class OrderCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartOrderSerializer

    def post(self, request, *args, **kwargs):
        cart = Cart.objects.filter(user=request.user).first()
        if cart is None:
            return Response({'error': 'Your cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)
        order = CartOrder.objects.create(user=request.user, cartOrder=cart, total_price=cart.total_price, shipping_address=request.data.get('shipping_address'))
        for item in cart.cart_items.all():
            CartItem.objects.create(order=order, product=item.product, quantity=item.quantity)
        cart.delete()
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    