from django.urls import path, include
from android.views import *


urlpatterns = [
    path('an_landing/', an_landing, name='an_landing'),
    path('an_product/<str:id>', an_product, name='an_product'),
]   

