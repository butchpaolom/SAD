from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from .models import *
from django.conf import settings
from .serializer import *
from .forms import *
from django.views.generic import ListView, TemplateView, UpdateView, CreateView, DeleteView
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt

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

        product_name = Product.objects.get(id=int(product)).product_name
        price = Product.objects.get(id=int(product)).price

    new_order = {
        "id": product,
        "product": product_name,
        "quantity": quantity,
        "image": image,
        "total_price": str(price * int(quantity)),
    }

    try:
        cart = request.session['cart']
        for i in range(len(cart)):
            if cart[i]['id'] == new_order['id']: #replace changes if existing (for ex. quantity)
                cart[i] = new_order
                request.session['cart'] = cart
                success = True
                message = 'Cart Updated: The quantity of <strong>{0}</strong> is changed to <strong>{1}</strong>.'.format(new_order['product'], new_order['quantity'])
                data = {
                    "success": success,
                    "message": message
                }
                return JsonResponse(data)

        cart.append(new_order)
        request.session['cart'] = cart
    except:
        request.session['cart'] = []
        cart = request.session['cart']
        cart.append(new_order)
        request.session['cart'] = cart

    success = True
    message = 'Successfully added <strong>{0} ({1})</strong> to cart.'.format(new_order['product'], new_order['quantity'])
    data = {
        "success": success,
        "message": message
    }
    return JsonResponse(data)

def clear_cart(request):
    try:
        request.session['cart']=[]
        message = "Cart is now empty!"
        print('Cart is cleared')
    except:
        message = "Try again."

    data = {
        "message": message
    }

    return JsonResponse(data)

def create_customer_info(request):
    success = False
    if request.method == 'POST':
        post_data = request.POST.copy()


        #create intial order from request.session['cart']
        orders=[]
        cart = request.session['cart']
        for each in cart:
            order = InitialOrder(
                product=Product.objects.get(id=each['id']),
                quantity=each['quantity'],
                total_price= Product.objects.get(id=each['id']).price*int(each['quantity']))
            order.save()
            orders.append(order)

        #create final order from inital order list 'orders'

        finalOrder = FinalOrder()
        finalOrder.save()
        overall_price=0
        for each in orders:
            overall_price = overall_price + each.total_price
            finalOrder.overall_price = overall_price
            finalOrder.orders.add(each)
            finalOrder.save()
        
        post_data['final_order'] = str(finalOrder.id)
        request.session['trans_id'] = str(finalOrder.trans_id)
        print(post_data)
        form = CustomerInfoForm(post_data)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            success = True
            data = {
                "success": success,
                "method": post_data['payment_method']
            }
        else:
            success= False
            data = {
                "success": success
            }
    return JsonResponse(data)



 
        









