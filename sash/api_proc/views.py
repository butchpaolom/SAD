from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from .models import *
from django.conf import settings
from .serializer import *
from .forms import *
from django.views.generic import ListView, TemplateView, UpdateView, CreateView, DeleteView
from decimal import Decimal
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import threading

# Create your views here.


def landing(request):
    products = Product.objects.all()
    data = ProductSerializer(products, many=True)
    return JsonResponse(data.data, safe=False)

def products_cat(request, category):
    if category == "all":
        products = Product.objects.all()
    else:
        products = Product.objects.filter(category__category_name=category)
    data = ProductSerializer(products, many=True)
    return JsonResponse(data.data, safe=False)  

def product_detail(request, id):
    product = Product.objects.get(id=id)
    product.views = product.views + 1
    product.save()
    print(product)
    data = ProductSerializer(product)
    return JsonResponse(data.data)

def create_order(request):
    if request.method == 'POST':
        product = request.POST['product']
        quantity = request.POST['quantity']
        image = request.POST['image']
        
        if int(quantity) > Product.objects.get(id=int(product)).stock:
            success = False
            message = 'Sorry, the product is out of stock.'
            data = {
            "success": success,
            "message": message
                }
            return JsonResponse(data)

        product_name = Product.objects.get(id=int(product)).product_name
        price = Product.objects.get(id=int(product)).price
        delivery_price = Product.objects.get(id=int(product)).delivery_price

    new_order = {
        "id": product,
        "product": product_name,
        "quantity": str(quantity),
        "image": image,
        "price": str(price),
        "delivery_price": str(delivery_price),
        "total_price": '{:.2f}'.format((price+delivery_price)*abs(int(quantity))),
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

def send_email(data):
    final_order = FinalOrder.objects.get(id=data['final_order'])
    subject = 'We received your order!'
    html_message = render_to_string('email.html', {'data': data, 'final_order': final_order})
    plain_message = strip_tags(html_message)
    from_email = 'realtantan7@gmail.com'
    to = data['email']

    mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def create_customer_info(request):
    success = False
    if request.method == 'POST':
        post_data = request.POST.copy()

        #create intial order from request.session['cart']
        orders=[]

        #server side possible from localStorage of cart which contains new order, line 58
        cart = request.session['cart']
        for each in cart:
            order = InitialOrder(
                product=Product.objects.get(id=each['id']),
                quantity=each['quantity'],
                total_price= (Product.objects.get(id=each['id']).delivery_price + Product.objects.get(id=each['id']).price)*int(each['quantity']))
            order.save()
            orders.append(order)

        #create final order from inital order list 'orders'

        finalOrder = FinalOrder()
        finalOrder.save() #Final order is created 
        overall_price=0
        for each in orders:
            overall_price = overall_price + each.total_price
            finalOrder.overall_price = overall_price
            finalOrder.orders.add(each)
            finalOrder.save()
        
        post_data['final_order'] = str(finalOrder.id)
        request.session['trans_id'] = str(finalOrder.trans_id) #stores transaction_id in session -> make client side equivalent in new_gen
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
            request.session['cart']=[]
        else:
            success= False
            data = {
                "success": success
            }

    thread_list = []
    thread = threading.Thread(target=send_email, args=(post_data,))
    thread_list.append(thread)
    thread.start()
    return JsonResponse(data)


def get_cart(request):
    try:
        cart = request.session['cart']
    except:
        request.session['cart'] = []
        cart = request.session['cart']

    data = {
        "cart": cart,
    }

    return JsonResponse(data)


 
        









