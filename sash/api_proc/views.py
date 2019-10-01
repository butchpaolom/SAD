from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .models import *
from .serializer import *
from django.views.generic import ListView, TemplateView, UpdateView, CreateView, DeleteView


# Create your views here.

def landing(request):
    products = Product.objects.all()
    data = ProductSerializer(products, many=True)
    print(data)
    return JsonResponse(data.data, safe=False)

def product_detail(request, id):
    product = Product.objects.get(id=id)
    print(product)
    data = ProductSerializer(product)
    return JsonResponse(data.data)

def create_order(request):
    if request.method == 'POST':
        product = request.POST['product']
        quantity = request.POST['quantity']
        image = request.POST['image']

    new_order = {
        "product": product,
        "quantity": quantity,
        "image": image,
    }

    try:
        cart = request.session['cart']
        cart.append(new_order)
        request.session['cart'] = cart
    except:
        request.session['cart'] = []
        cart = request.session['cart']
        cart.append(new_order)
        request.session['cart'] = cart

    return JsonResponse(new_order)

def clear_cart(request):
    print(request.session['cart'])
    request.session.clear()
    print('Session is cleared.')

    return HttpResponse(200)

