from rest_framework import serializers
from .models import *

class ProductSerializer(serializers.ModelSerializer):
    available = serializers.BooleanField(source='in_stock')
    category = serializers.CharField(source='category_name')
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'description', 'category', 'product_image', 'price', 'available', 'stock']


