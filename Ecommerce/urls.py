from django.urls import path,include
from django.contrib import admin
import Ecommerce.views as views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter


# router = DefaultRouter()
# router.register('files', FilesViewSet, basename='files')

urlpatterns = [
    # path('api/', include(router.urls)),
    
    path('hello/', views.hello, name='hello'),
    path('user_signup/', views.user_signup, name='user_signup'),
    path('user_login/', views.user_login, name='user_login'),
    path('upload_product/', views.upload_product, name='upload_product'),
    path('seller_signup/', views.seller_signup, name='seller_signup'),
    path('seller_login/', views.seller_login, name='seller_login'),
    path('get_products_default_50/', views.get_products_default_50, name='get_products_default_50'),
    path('get_products_by_category/', views.get_products_by_category, name='get_products_by_category'),
    path('get_product_by_filtered_value/', views.get_product_by_filtered_value, name='get_product_by_filtered_value'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('get_cart_items/', views.get_cart_items, name='get_cart_items'),
    path('number_of_items_in_cart_user/', views.number_of_items_in_cart_user, name='number_of_items_in_cart_user'),
    path('get_user_cart_products/', views.get_user_cart_products, name='get_user_cart_products'),
    path('remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),
    path('get_user_name/', views.get_user_name, name='get_user_name'),
    path('add_user_address/', views.add_user_address, name='add_user_address'),
    path('get_user_details/', views.get_user_details, name='get_user_details'),
    path('update_user_details/', views.update_user_details, name='update_user_details'),
    path('send_email_update_otp/', views.send_email_update_otp, name='send_email_update_otp'),
    path('update_user_email/', views.update_user_email, name='update_user_email'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
