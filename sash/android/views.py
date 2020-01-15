from django.shortcuts import render
from front_ep.models import *
import json
import requests

# Create your views here.

def an_landing(request):
    return render(request, 'landing_android.html')

def an_product(request, id):
    base_url = "{0}://{1}".format(request.scheme, request.get_host())
    api_url = base_url + '/new_api/api_products/' + id
    r = requests.get(api_url)
    data = r.json()
    print(data)
    return render(request, 'product_android.html', data)