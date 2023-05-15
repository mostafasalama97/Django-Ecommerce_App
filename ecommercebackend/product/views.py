import datetime
from django.shortcuts import render, get_object_or_404
from rest_framework import generics, filters, status
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly ,AllowAny
from django_filters.rest_framework import DjangoFilterBackend

# Retrieve and list products by category and search by keywords
class ProductListByCategory(generics.ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['productName', 'productID']
    ordering_fields = ['productName', 'productPrice']

    def get_queryset(self):
        category = self.kwargs['category']
        queryset = Products.objects.filter(category=category)
        return queryset

# List all categories
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer


# List all products

class ProductList(generics.ListAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    page_size = 10

# Update or delete a product
class ProductUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'productID'

    def delete(self, request, *args, **kwargs):
        productID = self.kwargs['productID']
        product = get_object_or_404(Products, productID=productID)
        product.delete()
        return Response({'message': 'Product deleted'}, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        productID = self.kwargs['productID']
        product = get_object_or_404(Products, productID=productID)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Product updated', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Retrieve, update, or delete a product
class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [AllowAny]
    lookup_field = 'productName'


    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

# Create a product

class ProductCreateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [AllowAny]
    lookup_field = 'productID'
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


