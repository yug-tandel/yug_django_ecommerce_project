from django.urls import path
from . views import *

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('product/', product, name='product'),
    path('product_detail/', product_detail, name='product_detail'),
    path('shoping_cart/', shoping_cart, name='shoping_cart'),
    path('blog/', blog, name='blog'),
    path('blog_detail/', blog_detail, name='blog_detail'),
    path('register/', register, name='register'),
    path('otp/', otp, name='otp'),
    path('login/',login, name='login'),
    path('logout/',logout, name='logout'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('edit_profile/',edit_profile, name='edit_profile'),
    path('reset_password/', reset_password, name='reset_password'),
    path('add_to_wishlist/<int:pk>', add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:pk>/<str:string>', remove_from_wishlist, name='remove_from_wishlist'),
    path('my_wishlist/',my_wishlist, name='my_wishlist'),
    path('add_to_cart/<int:pk>/<str:string>',add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:pk>',remove_from_cart, name='remove_from_cart'),
    path('shoping_cart/paymenthandler/', paymenthandler, name='paymenthandler'),
]