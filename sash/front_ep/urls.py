from django.urls import path, include
from .views import *

urlpatterns = [
    path('', landing, name='landing'),
    path('products/<str:category>', products, name='category'),
    path('product/<int:id>', product_detail, name='product_detail'),
    path('cart_inside/', cart_view, name='cart_view'),
    path('cart/', cart_base, name='cart_base'),
    path('order_form', customer_form, name='customer_form'),
    path('about', about, name='about')
    ]   
