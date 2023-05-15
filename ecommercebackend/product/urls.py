from django.urls import path
from django.views import View
from .views import *
from . import views

urlpatterns = [
    path('product/<str:category>/', ProductListByCategory.as_view(), name='ProductListByCategory'), #if i will list using filteration
    path('productlist', ProductList.as_view(), name='ProductList'),
    path('productdetails/<int:productID>/', ProductUpdateDelete.as_view(), name='ProductUpdateDelete'),
    path('productdetailsss/<str:productName>/detail/', ProductRetrieveUpdateDestroyView.as_view(), name='ProductRetrieveUpdateDestroyView'),
    path('create/<int:productID>', ProductCreateView.as_view(), name='ProductCreateView'),
]
