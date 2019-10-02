from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Product)
admin.site.register(InitialOrder)
admin.site.register(FinalOrder)
admin.site.register(CustomerInfo)
admin.site.register(Category)
admin.site.register(Transaction)