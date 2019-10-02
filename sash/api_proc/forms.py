from django import forms
from api_proc.models import *
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit



class CustomerInfoForm(forms.ModelForm):
    class Meta:
        model = CustomerInfo
        fields = '__all__'
        widgets = {'final_order': forms.HiddenInput()}


