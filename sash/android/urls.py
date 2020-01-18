from django.urls import path, include
from android.views import *


urlpatterns = [
    path('', an_landing, name='an_landing'),
    path('cart', an_cart, name='an_cart'),
]   

