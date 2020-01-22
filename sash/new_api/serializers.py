from rest_framework import serializers
from api_proc.models import *
from front_ep.models import *




#done
class ProductSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.CharField(source='category_name')
    class Meta:
        model = Product
        fields = ['url', 'id', 'product_name', 'description', 'category', 'product_image', 'product_image1', 'product_image2', 'price', 'stock', 'delivery_price', 'views']
#done
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name','image']

class InitialOrderSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='product.product_name')
    delivery = serializers.DecimalField(source='product.delivery_price', max_digits=10, decimal_places=2)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2)
    class Meta:
        model = InitialOrder
        fields = ['product', 'quantity', 'total_price','delivery', 'product_price']

class FinalOrderSerializer(serializers.ModelSerializer):
    orders = InitialOrderSerializer(many=True)
    payment_method = serializers.CharField(source='get_payment_method_display')
    class Meta:
        model = FinalOrder
        fields = ['orders', 'overall_price', 'trans_id', 'payment_method']

class CustomerInfoSerializerGet(serializers.ModelSerializer):
    final_order = FinalOrderSerializer()
    class Meta:
        model = CustomerInfo
        fields = ['final_order', 'address', 'first_name', 'last_name', 'middle_initial', 'contact_number', 'email', 'date_ordered']

class CustomerInfoSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = CustomerInfo
        fields = ['final_order', 'address', 'first_name', 'last_name', 'middle_initial', 'contact_number', 'email', 'date_ordered', 'payment_method']


class TransactionSerializer(serializers.ModelSerializer):
    final_order = FinalOrderSerializer()
    status = serializers.CharField(source='get_status_display')
    class Meta:
        model = Transaction
        fields = ['id' , 'final_order', 'paid', 'status']


class FrontAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrontAsset
        fields = ['car_img1', 'car_img2', 'car_img3', 'company_name', 'company_logo', 'address', 'colorscheme']




