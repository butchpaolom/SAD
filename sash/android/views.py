from django.shortcuts import render
from front_ep.models import *
import json
import requests

# Create your views here.

def an_landing(request):
    return render(request, 'landing_android.html')
