from django.db import models
from seller.models import *
# Create your models here.

class Buyer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15,null=True,blank=True)
    password = models.CharField(max_length=50)
    address = models.CharField(max_length=250,blank=True)
    pic = models.FileField(upload_to='buyer_profile_pics', default='avtar.jpg')
    
    def __str__(self):
        return self.email
    

class Wishlist(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1,null=True,blank=True)

    class Meta:
        unique_together = ('buyer', 'product')
        

    def __str__(self):
        return f'{self.buyer.email} --> {self.product.product_name}'
    
    
class Cart(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, null=True,blank=True)   

    class Meta:
        unique_together = ('buyer','product') 

    def __str__(self):
        return f'{self.buyer.email} --> {self.product.product_name}'