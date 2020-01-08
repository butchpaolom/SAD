from rest_framework import serializers
from api_proc.models import *

#done
class ProductSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.CharField(source='category_name')
    class Meta:
        model = Product
        fields = ['url', 'id', 'product_name', 'description', 'category', 'product_image', 'product_image1', 'product_image2', 'price', 'stock']
#done
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name']

class CustomerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = CustomerInfo
        fields = ['final_order', 'address', 'first_name', 'last_name', 'middle_initial', 'contact_number', 'email', 'date_ordered']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id' , 'final_order', 'paid', 'delivery_date', 'delivered_date']
        depth = 3