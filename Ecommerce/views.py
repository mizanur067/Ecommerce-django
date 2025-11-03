from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.decorators import api_view,parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from .Serializers import ProductSerializer
from .models import User_signup_details, product_details, seller_sign_up_details,User_cart,user_address
from rest_framework import status
from django.contrib.auth.hashers import check_password,make_password
from .Serializers import UserCartSerializer
# from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
import random
from django.core.cache import cache
# Create your views here.
def hello(request):
    return HttpResponse("Hello, world. You're at the Ecommerce index.")

@api_view(['POST'])
def user_signup(request):
    name= request.data.get('name')
    email= request.data.get('email')
    password= request.data.get('password')

    user = User_signup_details(name=name, email=email, password=make_password(password))
    user.save()

    return Response({"message": "User signed up successfully."})

@api_view(['POST'])
def user_login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = User_signup_details.objects.get(email=email)
        if check_password(password, user.password):
            return Response({"message": "Login successful."})
        else:
            return Response({"message": "Invalid credentials."})
    except User_signup_details.DoesNotExist:
        return Response({"message": "User does not exist."})

@api_view(['POST'])
def get_user_details(request):
    email = request.data.get('email')

    try:
        user = User_signup_details.objects.get(email=email)
        user_data = {
            "email": user.email,
            "name": user.name,
            "phone_number": user.phone_number,
            "Gender": user.Gender
        }
        return Response({"user_data": user_data})
    except User_signup_details.DoesNotExist:
        return Response({"message": "User does not exist."}, status=404)
#update name and gender
@api_view(['POST'])
def update_user_details(request):
    email = request.data.get('email')
    name = request.data.get('name')
    gender = request.data.get('Gender')
    
    try:
        user = User_signup_details.objects.get(email=email)
        user.name = name
        user.Gender = gender
        user.save()
        return Response({"message": "User details updated successfully."})
    except User_signup_details.DoesNotExist:
        return Response({"message": "User does not exist."}, status=404)



# Temporary in-memory OTP storage (use cache/DB in production)
otp_storage = {}

@api_view(['POST'])
def send_email_update_otp(request):
    new_email = request.data.get('new_email')

    if not new_email:
        return Response({"message": "New email required."}, status=400)

    otp = random.randint(100000, 999999)

    # Store OTP in cache for 10 minutes (600 seconds)
    cache.set(f"email_otp_{new_email}", otp, timeout=600)

    # Send OTP to the new email
    print(f"Sending OTP {otp} to email {new_email}")  # For debugging; remove in production
    send_mail(
        subject="Email Verification OTP",
        message=f"Your OTP for updating email is: {otp}\n\nThis OTP is valid for 10 minutes.",
        from_email="mizanuranr@gmail.com",
        recipient_list=[new_email],
        fail_silently=False,
    )

    return Response({"message": "OTP sent to new email and valid for 10 minutes."})


@api_view(['POST'])
def update_user_email(request):
    email = request.data.get('email')
    new_email = request.data.get('new_email')
    otp = request.data.get('otp')

    if not all([email, new_email, otp]):
        return Response({"message": "Email, new_email, and OTP are required."}, status=400)

    # Retrieve OTP from cache
    cached_otp = cache.get(f"email_otp_{new_email}")

    if not cached_otp:
        return Response({"message": "OTP expired or not found."}, status=400)

    if str(cached_otp) != str(otp):
        return Response({"message": "Invalid OTP."}, status=400)

    # OTP verified — update user email
    try:
        user = User_signup_details.objects.get(email=email)
        user.email = new_email
        user.save()
        cache.delete(f"email_otp_{new_email}")  # remove used OTP
        return Response({"message": "User email updated successfully."})
    except User_signup_details.DoesNotExist:
        return Response({"message": "User does not exist."}, status=404)



@api_view(['POST'])
def seller_signup(request):
    name = request.data.get('name')
    email = request.data.get('email')
    shopname = request.data.get('shopname')
    shop_description = request.data.get('shop_description')
    phone_number = request.data.get('phone_number')
    address = request.data.get('address')
    password = request.data.get('password')

    seller = seller_sign_up_details(
        name=name,
        email=email,
        shopname=shopname,
        shop_description=shop_description,
        phone_number=phone_number,
        address=address,
        password=make_password(password)
    )
    seller.save()

    return Response({"message": "Seller signed up successfully."})


@api_view(['POST'])
def seller_login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        seller = seller_sign_up_details.objects.get(email=email)
        if check_password(password, seller.password):
            return Response({"message": "Seller login successful."})
        else:
            return Response({"message": "Invalid credentials."})
    except seller_sign_up_details.DoesNotExist:
        return Response({"message": "Seller does not exist."})


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])  # Needed for image uploads
def upload_product(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# get the list of products
@api_view(['GET'])
def get_products_default_50(request):
    products = product_details.objects.all()[:50]   
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_products_by_category(request):
    category = request.data.get('category')
    products = product_details.objects.filter(category=category)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_product_by_filtered_value(request):
    search = request.data.get('search')
    products = (product_details.objects.filter(desc__icontains=search) | product_details.objects.filter(title__icontains=search) | product_details.objects.filter(category__icontains=search))[:50]
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User_cart

@api_view(['POST'])
def add_to_cart(request):
    user_email = request.data.get('user_email')
    product_id = request.data.get('product_id')

    if not user_email or not product_id:
        return Response({"error": "Missing user_email or product_id"}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the product already exists in the user's cart
    if User_cart.objects.filter(user_email=user_email, Product_id=product_id).exists():
        return Response({"message": "Product already in cart."}, status=status.HTTP_400_BAD_REQUEST)

    # Add to cart
    try:
        new_cart = User_cart(user_email=user_email, Product_id=product_id)
        new_cart.save()
        return Response({"message": "Product added to cart."}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def remove_from_cart(request):
    user_email = request.data.get('user_email')
    Product_id = request.data.get('Product_id')

    if not user_email or not Product_id:
        return Response({"error": "Missing user_email or Product_id"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        cart_item = User_cart.objects.get(user_email=user_email, Product_id=Product_id)
        cart_item.delete()
        return Response({"message": "Product removed from cart."}, status=status.HTTP_200_OK)
    except User_cart.DoesNotExist:
        return Response({"message": "Product not found in cart."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def get_cart_items(request):
    user_email = request.data.get('user_email')

    if not user_email:
        return Response({"message": "Missing user_email"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        cart_items = User_cart.objects.filter(user_email=user_email)
        if not cart_items:
            return Response({"message": "No items in cart."}, status=status.HTTP_404_NOT_FOUND)

        serialized_cart = UserCartSerializer(cart_items, many=True)
        return Response({"message": "Cart items retrieved successfully", "data": serialized_cart.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    
@api_view(['POST'])
def number_of_items_in_cart_user(request):
    try:
        email=request.data.get('user_email')
        count = User_cart.objects.filter(user_email=email).count()
        return Response({"count": count}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
def get_user_cart_products(request):
    product_id = request.data.get('product_id')


    try:
        products = product_details.objects.filter(id=product_id)
        if not products:
            return Response({"message": "No product found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def get_user_name(request):
    email=request.data.get('email')
    try:
        user= User_signup_details.objects.get(email=email)
        name=user.name
        return Response({"name":name}, status=status.HTTP_200_OK)
    except User_signup_details.DoesNotExist:
        return Response({"message": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['POST'])
def add_user_address(request):
    try:
        user_email = request.data.get('user_email')
        name = request.data.get('name')
        phone_number = request.data.get('phone_number')
        address_line1 = request.data.get('address_line1')
        address_line2 = request.data.get('address_line2')
        city = request.data.get('city')
        state = request.data.get('state')
        postal_code = request.data.get('postal_code')
        country = request.data.get('country')
        add= user_address.objects.filter(user_email=user_email,postal_code=postal_code,address_line1=address_line1)
        if add.exists():
            return Response({"message": "Address already exists."})
        address = user_address(
            user_email=user_email,
            name=name,
            phone_number=phone_number,
            address_line1=address_line1,
            address_line2=address_line2,
            city=city,
            state=state,
            postal_code=postal_code,
            country=country
        )
        address.save()

        return Response({"message": "Address saved successfully."})
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)