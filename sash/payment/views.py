from django.shortcuts import render
from django.urls import reverse
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
from api_proc.models import *
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm

# Create your views here.

#test
def payment_process(request):
    trans_id = request.session['trans_id']
    print(trans_id)
    order = FinalOrder.objects.get(trans_id=trans_id)
    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % order.overall_price.quantize(Decimal('.01')),
        'item_name': 'Order ID: {}'.format(order.trans_id),
        'invoice': str(trans_id),
        'currency_code': 'PHP',
        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host, reverse('payment_cancelled')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'process.html', {'order':order,'form':form})

@csrf_exempt
def payment_done(request):
    print(request.POST)
    return render(request, 'done.html')

@csrf_exempt
def payment_cancelled(request):
    return render(request, 'cancelled.html')
