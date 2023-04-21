from django.db import models
# Create your models here.


class Seller(models.Model):
    user_name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    address = models.TextField(max_length=250,blank=True, null=True)
    password = models.CharField(max_length=50)
    pic = models.FileField(upload_to='seller_profile_pic', default='avtar.jpg', blank=True,null=True)


    def __str__(self):
        return self.email
    
class Product(models.Model):
    product_choice = [
        ('men','men'),
        ('women','women'),
        ('shoes','shoes'),
        ('watches','watches'),
        ('bag','bag')
    ]

    product_name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=8,decimal_places=2,default=10)
    des = models.TextField(max_length=500)
    product_stock = models.IntegerField(default=0)
    product_pic = models.FileField(upload_to='product_images',default='pro.jpg')
    seller = models.ForeignKey(Seller,on_delete=models.CASCADE)
    category = models.CharField(max_length = 10, choices=product_choice,null=True,blank=True)




    def __str__(self):
        return self.product_name
    


class MyOrders(models.Model):
    buyer = models.ForeignKey(to = 'buyer.Buyer', on_delete=models.CASCADE)
    purchased_date = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     self.buyer


class OrderedProducts(models.Model):
    my_order = models.ForeignKey(MyOrders, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    total_amount = models.FloatField()
