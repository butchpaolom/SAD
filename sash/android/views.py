from django.shortcuts import render
from front_ep.models import *
import json
import requests
from api_proc.forms import CustomerInfoForm
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def an_landing(request):
    return render(request, 'landing_android.html')

def an_cart(request):
    return render(request, 'cart_android.html')

def an_order_form(request):
    return render(request, 'android_order_form.html', {'form':CustomerInfoForm})

@csrf_exempt
def an_payment_done(request):
    return render(request, 'done_payment_android.html')

@csrf_exempt
def an_payment_cancelled(request):
    return render(request, 'cancelled_payment_android.html')

def an_transactions(request):
    return render(request, 'transactions_android.html')
