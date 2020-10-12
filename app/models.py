from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    Category_name= models.CharField(max_length=1000)

    def __str__(self):
        return self.Category_name


class addproduct(models.Model):
    freeze_choice = (
        ('yes','Yes'),
        ('no','No')
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    sku = models.CharField(max_length=200)
    Product_link = models.CharField(max_length=2000)
    min_price= models.FloatField()  
    our_category = models.ForeignKey(Category,on_delete=models.CASCADE)
    Freezed = models.CharField(max_length=20,default="no",choices=freeze_choice)

    def __str__(self):
        return self.sku


class temp(models.Model):
    sku = models.CharField(max_length=200)
    link = models.CharField(max_length=400)
    web_price = models.CharField(max_length = 40)
    our_price = models.CharField(max_length=40)
    offers = models.CharField(max_length=40)
    express= models.CharField(max_length=40)
    sot = models.CharField(max_length=500)
    time = models.DateTimeField(auto_now=True)
