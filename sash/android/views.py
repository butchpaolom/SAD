from django.shortcuts import render
from front_ep.models import *
import json
import requests
from api_proc.forms import CustomerInfoForm

# Create your views here.

def an_landing(request):
    return render(request, 'landing_android.html')

def an_cart(request):
    return render(request, 'cart_android.html')

def an_order_form(request):
    return render(request, 'android_order_form.html', {'form':CustomerInfoForm})
