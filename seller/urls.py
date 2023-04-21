from django.urls import path
from .views import *

urlpatterns = [
    path('', seller_index, name='seller_index'),
    path('show_product/', show_product, name='show_product'),
    path('seller_register/', seller_register, name='seller_register'),
    path('seller_otp/', seller_otp, name='seller_otp'),
    path('seller_login/', seller_login, name='seller_login'),
    path('seller_logout/',seller_logout, name='seller_logout'),
    path('seller_edit_profile/',seller_edit_profile, name='seller_edit_profile'),
    path('seller_forgot_password/',seller_forgot_password, name='seller_forgot_password'),
    path('seller_reset_password/',seller_reset_password, name='seller_reset_password'),
    path('buttons/',buttons, name='buttons'),
    path('forms/',forms, name='forms'),
    path('add_product/',add_product, name='add_product'),
    path('edit_product/<int:pk>',edit_product, name='edit_product'),
    path('delete_product/<int:pk>', delete_product, name='delete_product'),
    path('ordered_products',ordered_products, name='ordered_products')
]