from django.urls import path, include
from android.views import *


urlpatterns = [
    path('', an_landing, name='an_landing'),
    path('cart', an_cart, name='an_cart'),
    path('form', an_order_form, name='an_order_form'),
    path('transactions', an_transactions, name='an_transactions'),
    path('done/', an_payment_done, name='an_payment_done'),
    path('cancelled/', an_payment_cancelled, name='an_payment_cancelled'),
    path('about/', an_about, name='an_about'),
]   

