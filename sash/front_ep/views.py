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
    cat_all = Category.objects.all()
    category = cat_all.order_by('?')[:5]
    context = {
        'asset': asset,
        'category': category,
        'cat': cat_all,
    }
    print(category)
    return render(request, 'landing.html', context)

def products(request,categoryr):
    asset = FrontAsset.objects.first()
    category = Category.objects.all()
    cat_list = category.order_by('?')[:5]
    cats = ['all']
    for each in category:
        cats.append(each.category_name)

    if categoryr not in cats:
        return redirect('landing')

    base_url = "{0}://{1}".format(request.scheme, request.get_host())
    api_url = base_url + '/api/products_category/' + str(categoryr)

    start_time = time.time()
    session = requests.session()
    r = session.get(api_url)
    print("%sseconds " %(time.time() - start_time))
    products = r.json()

    if str(categoryr) == "all":
        categoryr = "All Products"

    data = {
        "products": products,
        "category": categoryr,
        'cat': cat_list,
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
    category = Category.objects.all().order_by('?')[:5]
    context = {
        'category': category,
        'asset': asset
    }
    return render(request, 'about.html', context)
