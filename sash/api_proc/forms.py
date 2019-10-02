from django import forms
from api_proc.models import *
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit



class CustomerInfoForm(forms.ModelForm):
    payment_method = forms.ChoiceField(choices=((1,"Cash on delivery"),(2,"PayPal")))
    class Meta:
        model = CustomerInfo
        fields = '__all__'
        widgets = {'final_order': forms.HiddenInput()}


