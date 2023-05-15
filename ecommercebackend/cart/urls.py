from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('cart/', CartAPIView.as_view(), name='cart'),
    path('add/<int:productID>/', CartAPIView.as_view(), name='add_to_cart'),
    path('remove/<int:cart_item_id>/', CartAPIView.as_view(), name='remove_from_cart'),
    path('update/<int:cart_item_id>/', CartAPIView.as_view(), name='update_cart_item'),
    path('cartcreate/create/', OrderCreateView.as_view(), name='create_order'),

]
