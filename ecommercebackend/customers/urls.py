from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('customers/', CustomerList.as_view(), name='CustomerList'),
    path('<int:customer_ID>/', CustomerDetail.as_view(), name='CustomerDetail'),
    path('customers/<int:customer_ID>/wishlist/', CustomerWishList.as_view(), name='CustomerWishList'),
    path('wishlist/', WishlistList.as_view(), name='WishlistList'),
    path('wishlist/<int:wishlist_owner__customer_ID>/', WishlistDetail.as_view(), name='WishlistDetail'),
    path('orders/<int:pk>/', OrderDetail.as_view(), name='OrderDetail'),
    path('orders/addproduct/', AddProductToOrder.as_view(), name='AddProductToOrder'),
]

