from django.shortcuts import render, HttpResponse, redirect
from api_proc.models import *
import requests
import json
import time
import requests
from front_ep.models import *
from api_proc.forms import *

# Create your views here.



def landing(request):
    asset = FrontAsset.objects.first()
    context = {
        'asset': asset
    }
    return render(request, 'landing.html', context)

def products(request,category):
    asset = FrontAsset.objects.first()
    if category not in ['all', 'doors', 'others', 'cabinets']:
        return redirect('landing')
    base_url = "{0}://{1}".format(request.scheme, request.get_host())
    api_url = base_url + '/api/products_category/' + str(category)

    start_time = time.time()
    session = requests.session()
    r = session.get(api_url)
    print("%sseconds " %(time.time() - start_time))
    products = r.json()

    if str(category) == "all":
        category = "All Products"

    data = {
        "products": products,
        "category": category,
        "asset": asset,
    }

    return render(request, 'products.html', data)

def product_detail(request, id):
    asset = FrontAsset.objects.first()
    
    base_url = "{0}://{1}".format(request.scheme, request.get_host())
    api_url = base_url + '/api/product/' + str(id)

    start_time = time.time()
    session = requests.session()
    r = session.get(api_url)
    print("%sseconds " %(time.time() - start_time))
    data = r.json()

    context = {
        "data": data,
        "asset": asset
    }

    return render(request, 'product_detail.html', context)

def cart_view(request):
    try:
        cart = request.session['cart']
    except:
        request.session['cart'] = []
        cart = request.session['cart']

    context = {
        "cart": cart
    }

    return render(request, 'cart.html', context)

def cart_base(request):
    asset = FrontAsset.objects.first()
    
    context = {
        'asset': asset
    }
    return render(request, 'cart_base.html', context)

def customer_form(request):
    return render(request, 'order_form.html', {'form':CustomerInfoForm})

def about(request):
    asset = FrontAsset.objects.first()
    
    context = {
        'asset': asset
    }
    return render(request, 'about.html', context)
