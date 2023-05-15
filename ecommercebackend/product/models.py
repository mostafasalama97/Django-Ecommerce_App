from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Categories(models.Model):
    categoryName = models.CharField(max_length=50)
    categoryDescription = models.TextField()

    def __str__(self):
        return self.categoryName




class Products (models.Model):
    productID = models.AutoField(primary_key=True)
    # primary_key = True if you do not want to use default field "id" given by django to your model
    productName = models.CharField(max_length=50)
    productCategory = models.ForeignKey(Categories, on_delete=models.CASCADE, default=1)
    # i will make here relation between productCategory in product app and categoryName in category models class
    productImage = models.ImageField()
    productPrice = models.IntegerField()
    productDescription = models.TextField()

    def __str__(self):
        return self.productName
    