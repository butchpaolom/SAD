from django.shortcuts import render, redirect
from api_proc.models import *
import requests
from django.views.generic import ListView, TemplateView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from bootstrap_modal_forms.mixins import PassRequestMixin
from django.contrib.messages.views import SuccessMessageMixin
from .forms import *
from django.contrib import messages

# Create your views here.

    
class AdminLanding(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'


#Product
class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'product_tables.html'
    context_object_name = 'products'



class ProductUpdateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Product
    template_name = 'update.html'
    success_url = reverse_lazy('admin_products')
    form_class = ProductForm
    

    def get_success_message(self, cleaned_data):
        product_name = Product.objects.get(id=self.kwargs.get('pk'))
        message = "Successfully updated " + str(product_name)
        return message

class ProductCreateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'create.html'
    form_class = ProductForm
    context_object_name = 'product'
    success_url = reverse_lazy('admin_products')

    def get_success_message(self, cleaned_data):
        message = "Successfully added " + str(self.object.product_name)
        return message 
    

class ProductDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Product
    context_object_name = 'product'
    success_url = reverse_lazy('admin_products')
    template_name = 'delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        context['model'] = self.model.__name__
        context['name'] = Product.objects.get(id=self.kwargs.get('pk')).product_name
        return context

    def delete(self, request, *args, **kwargs):
        product_name = Product.objects.get(id=self.kwargs.get('pk'))
        message = "Successfully deleted " + str(product_name)
        messages.warning(self.request, message)
        return super(ProductDeleteView, self).delete(request, *args, **kwargs)


#CustomerInfo
class CustomerInfoListView(LoginRequiredMixin, ListView):
    model = CustomerInfo
    template_name = 'customer_info_tables.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        context['customer_info'] = CustomerInfo.objects.all()
        return context