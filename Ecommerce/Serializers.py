# serializers.py
from rest_framework import serializers
from .models import User_cart, product_details, User_cart

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = product_details
        fields = '__all__'
class UserCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_cart
        fields = '__all__'