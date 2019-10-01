from django.urls import path, include
from .views import *

urlpatterns = [
    path('', landing, name='landing_api'),
    path('product/<int:id>', product_detail, name='product_detail'),
    path('add_to_cart/', create_order, name='create_order'),
    path('empty_cart/', clear_cart, name='clear_cart'),
]   
