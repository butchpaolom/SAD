from django import forms
from api_proc.models import *
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit
from django.contrib.auth.models import User



class ProductForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['views']

class TransactionDeliveryDateForm(PopRequestMixin, forms.ModelForm):
    delivery_date = forms.DateTimeField(
                input_formats = ['%Y-%m-%dT%H:%M'],
                widget = forms.DateTimeInput(
                    attrs={'type':'datetime-local'},
                    format='%Y-%m-%dT%H:%M')
                    )
    class Meta:
        model = Transaction
        fields = ['delivery_date']  

class TransactionDeliveredDateForm(PopRequestMixin, forms.ModelForm):
    delivered_date = forms.DateTimeField(
                input_formats = ['%Y-%m-%dT%H:%M'],
                widget = forms.DateTimeInput(
                    attrs={'type':'datetime-local'},
                    format='%Y-%m-%dT%H:%M')
                    )
    class Meta:
        model = Transaction
        fields = ['delivered_date'] 

class CashOnDeliveryUpdate(PopRequestMixin, forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['paid'] 

class CustomerInfoNameUpdate(PopRequestMixin, forms.ModelForm):
    class Meta:
        model = CustomerInfo
        fields = ['first_name', 'last_name', 'middle_initial']

class CustomerInfoAddressUpdate(PopRequestMixin, forms.ModelForm):
    class Meta:
        model = CustomerInfo
        fields = ['address']
