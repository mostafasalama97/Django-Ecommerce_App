from django.db import models
from product.models import Products

class Order(models.Model):
    # fields for the order model
    order_status = models.CharField(max_length=50)
    products = models.ManyToManyField(Products, through='OrderProduct', related_name='order')
    order_name = models.CharField(max_length=50)
    order_ID = models.AutoField(primary_key=True)
    order_date = models.DateTimeField(auto_now_add=True)

    
    
class Customer(models.Model):
    customer_ID = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=80)
    customer_phone_number = models.CharField(max_length=15)
    customer_address = models.CharField(max_length=50)
    customer_orders = models.ManyToManyField(Order)
    customer_wish_list = models.ManyToManyField(Products, related_name='wishlist')

    def __str__(self):
        return self.customer_name
    



class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class WishList(models.Model):
    wishlist_owner = models.ForeignKey(Customer, on_delete=models.CASCADE)
    wishlist_items = models.ManyToManyField(Products, related_name='wishlist_items')

    def __str__(self):
        return f"{self.wishlist_owner}'s wishlist"
