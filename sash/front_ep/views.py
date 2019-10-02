from django.shortcuts import render, HttpResponse, redirect
from api_proc.models import *
import requests
import json
import time
import urllib3
from api_proc.forms import *

# Create your views here.

def landing(request):
    return render(request, 'landing.html', {})

def products(request,category):
    products = Product.objects.filter(category__category_name=category)
    if category not in ['doors', 'cabinets', 'others']:
        return redirect('landing')
    else:
        category_name = "Our " + str(category)
        if category_name == 'Our others':
            category_name = 'Others'
    context = {
        'category': category_name,
        'products': products,
    }
    return render(request, 'products.html', context)

def product_detail(request, id):
    base_url = "{0}://{1}".format(request.scheme, request.get_host())
    api_url = base_url + '/api/product/' + str(id)

    start_time = time.time()
    http = urllib3.PoolManager()
    r = http.request('GET', api_url)
    print("%sseconds " %(time.time() - start_time))
    return render(request, 'product_detail.html', json.loads(r.data.decode('utf-8')))

def cart_view(request):
    try:
        cart = request.session['cart']
    except:
        request.session['cart'] = []
        cart = request.session['cart']

    context = {
        "cart": cart,
    }
    return render(request, 'cart.html', context)

def cart_base(request):
    try:
        cart = request.session['cart']
        if cart:
            empty = False
        else:
            empty = True
    except:
        empty = True

    context = {
        "empty": empty
    }

    return render(request, 'cart_base.html', context)

def customer_form(request):
    return render(request, 'order_form.html', {'form':CustomerInfoForm})