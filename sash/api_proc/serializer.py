from rest_framework import serializers
from .models import *

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category_name')
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'description', 'category', 'product_image', 'product_image1', 'product_image2', 'price', 'stock']


