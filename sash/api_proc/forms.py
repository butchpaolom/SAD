from django import forms
from api_proc.models import *
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit



class CustomerInfoForm(forms.ModelForm):
    class Meta:
        model = CustomerInfo
        fields = '__all__'
        labels = {
            'payment_method': 'Payment method',
        }
        widgets = {
            'final_order': forms.HiddenInput(),
            'contact_number': forms.NumberInput(),
            'payment_method': forms.Select(choices=((1,"Cash on delivery"),(2,"PayPal"))),
                }


