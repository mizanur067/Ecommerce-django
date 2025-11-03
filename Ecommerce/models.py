from django.db import models

# Create your models here.
class User_signup_details(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True, null=True,default=None)
    Gender = models.CharField(max_length=10, blank=True, null=True,default=None)    


class user_address(models.Model):
    user_email = models.EmailField(max_length=100, blank=False)
    name= models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20 , blank = False)
    country = models.CharField(max_length=100, blank=True, null=True)
    
    
    
def Products(instance, filename):
    import os
    import time

    base, ext = os.path.splitext(filename)
    timestamp = int(time.time())
    new_filename = f"{base}_{timestamp}{ext}"
    return f'products/{new_filename}'
class product_details(models.Model):
    seller_email=models.EmailField(max_length=40,blank=False,default='rohan@gmail.com')
    title=models.CharField(max_length=200,blank=False)
    price=models.FloatField()
    category=models.CharField(max_length=40,blank=False)
    desc=models.TextField(blank=True,null=True)
    image= models.FileField(upload_to=Products,max_length=250,null=True,default=None)
    available_quantity=models.IntegerField(default=1)




class seller_sign_up_details(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    shopname = models.CharField(max_length=100, blank=True, null=True)
    shop_description = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    password = models.CharField(max_length=100)

class User_cart(models.Model):
    user_email = models.EmailField(max_length=100)
    Product_id= models.CharField(max_length=100, blank=False)
    



