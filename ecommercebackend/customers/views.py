from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated

# Views for Customer Model

class AddProductToOrder(APIView):
    """
    Add a product to an order.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        required_fields = ['order_ID', 'productID','order_status','products','order_name','order_date' ]
        for field in required_fields:
            if field not in request.data:
                return Response({'error': f'{field} is required.'}, status=status.HTTP_400_BAD_REQUEST)

        order_ID = request.data['order_ID']
        productID = request.data['productID']
        order_status = request.data['order_status']
        products = request.data['products']
        order_name = request.data['order_name']
        order_date = request.data['order_date']
        # quantity = request.data['quantity']

        order = get_object_or_404(Order, id=order_ID)
        product = get_object_or_404(Products, id=productID)

        # Check if the requested quantity is available for the product
        # if quantity > product.quantity_available:
        #     return Response({'error': f'Only {product.quantity_available} units of {product.name} are available.'}, status=status.HTTP_400_BAD_REQUEST)

        # Update the order
        order_product, created = OrderProduct.objects.get_or_create(order=order, product=product)
        # if not created:
        #     order_product.quantity += quantity
        # else:
        #     order_product.quantity = quantity
        # order_product.save()

        # Update the product quantity
        # product.quantity_available -= quantity
        product.save()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)



class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a single instance of Customer model.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    lookup_field = 'customer_ID'  # specify the lookup field to use for retrieving a single instance

class CustomerList(generics.ListCreateAPIView):
    """
    List all instances of Customer model or create a new one.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

# Views for WishList Model

class WishlistDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a single instance of WishList model.
    """
    queryset = WishList.objects.all()
    serializer_class = CustomerWishListSerializer
    lookup_field = 'wishlist_owner__customer_ID'  # specify the lookup field to use for retrieving a single instance

class WishlistList(generics.ListCreateAPIView):
    """
    List all instances of WishList model or create a new one.
    """
    queryset = WishList.objects.all()
    serializer_class = CustomerWishListSerializer


class CustomerWishList(APIView):
    """
    API endpoint for adding, retrieving or deleting product from a customer's wishlist.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, customer_ID):
        """
        Retrieve a customer's wishlist.
        """
        customer = get_object_or_404(Customer, customer_ID=customer_ID)
        serializer = CustomerWishListSerializer(customer)
        return Response(serializer.data)

    def post(self, request, customer_ID):
        """
        Add a product to a customer's wishlist.
        """
        customer = get_object_or_404(Customer, customer_ID=customer_ID)
        productID = request.data.get('productID')
        if not productID:
            return Response({'error': 'productID not provided.'}, status=status.HTTP_400_BAD_REQUEST)
        product = get_object_or_404(Products, id=productID)
        customer.wish_list.add(product)
        serializer = CustomerWishListSerializer(customer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, customer_ID):
        """
        Delete a product from a customer's wishlist.
        """
        customer = get_object_or_404(Customer, customer_ID=customer_ID)
        productID = request.data.get('productID')
        if not productID:
            return Response({'error': 'productID not provided.'}, status=status.HTTP_400_BAD_REQUEST)
        product = get_object_or_404(Products, id=productID)
        customer.wish_list.remove(product)
        serializer = CustomerWishListSerializer(customer)
        return Response(serializer.data)


# Views for Order Model

class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a single instance of Order model.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        customer = self.request.user.customer  # get the customer from the authenticated user
        productID = self.request.data.get('productID')
        product = get_object_or_404(Products, id=productID)
        order = serializer.save()
        order_product = OrderProduct.objects.create(order=order, product=product)
        order_product.save()
        order.customer = customer
        order.save()
