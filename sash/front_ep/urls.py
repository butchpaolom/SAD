from django.urls import path, include
from .views import *

urlpatterns = [
    path('', landing, name='landing'),
    path('products/<str:category>', products, name='category'),
    path('product/<int:id>', product_detail, name='product_detail'),
    path('cart/', cart_view, name='cart_view')
]   
