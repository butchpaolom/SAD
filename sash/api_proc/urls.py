from django.urls import path, include
from .views import *


urlpatterns = [
    path('', landing, name='landing_api'),
    path('product/<int:id>', product_detail, name='api_product_detail'),
    path('add_to_cart/', create_order, name='create_order'),
    path('empty_cart/', clear_cart, name='clear_cart'),
    path('get_cart/', get_cart, name='get_cart'),
    path('create_customer_order', create_customer_info, name='create_customer_info'),
    path('products_category/<str:category>', products_cat, name='products_cat'),
]   
