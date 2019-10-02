from django.urls import path, include
from payment.views import *


urlpatterns = [
    path('process/', payment_process, name='payment_process'),
    path('done/', payment_done, name='payment_done'),
    path('cancelled/', payment_cancelled, name='payment_cancelled'),
]   
