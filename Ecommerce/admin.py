from django.contrib import admin
from .models import  User_signup_details, product_details, seller_sign_up_details, User_cart,user_address
# Register your models here.
admin.site.register(User_signup_details)
admin.site.register(product_details)
admin.site.register(seller_sign_up_details)
admin.site.register(User_cart)
admin.site.register(user_address)

