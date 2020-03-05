from django.shortcuts import render
from api_proc.models import *
from rest_framework import viewsets, permissions
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters
import django_filters
from rest_framework import generics
from rest_framework import status
from front_ep.models import *
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
import json
from .threader import *
from .filters import ProductFilterSet, ProductOrder
# Create your views here.

class FrontAssetView(generics.RetrieveAPIView):
    queryset = FrontAsset.objects.all()
    serializer_class = FrontAssetSerializer

class ProductView(viewsets.ModelViewSet):
    search_fields = ['category__category_name', 'product_name']
    # filter_fields = ['category__category_name', 'product_name', 'price']
    ordering_fields = ['views', 'price']
    queryset = Product.objects.all().exclude(hidden=True)
    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend, ProductOrder]
    filter_class = ProductFilterSet
    
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        self.object = self.get_object()
        print(self.object.id)
        product = Product.objects.get(id=self.object.id)
        product.views += 1
        for each in Product.objects.all():
            if each.product_name == product.product_name:
                each.views = product.views
        do_thread(product.save(), arg=None)
        serializer = self.get_serializer(self.object)
        return Response(serializer.data)
    

class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# class CustomerInfoView

class CustomerInfoView(viewsets.ModelViewSet):
    queryset = CustomerInfo.objects.all()
    serializer_class = CustomerInfoSerializerGet
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]

        return [permission() for permission in permission_classes]
    
    def create(self, request):
        data = request.data.copy()
        print(data)
        return_data = ""
        try:
            cart = json.loads(data['cart'])
            print(cart)
            orders=[]
            for each in cart:
                prd = Product.objects.get(id=each['id'])
                print(prd)
                order = InitialOrder(
                    product=prd,
                    quantity=each['quantity'],
                    total_price= (float(prd.delivery_price) + prd.t_price())*int(each['quantity'])
                    )
                order.save()
                orders.append(order)
            
            finalOrder = FinalOrder()
            finalOrder.payment_method = data['payment_method']
            finalOrder.save() #Final order is created 
            overall_price=0
            for each in orders:
                overall_price = overall_price + each.total_price
                finalOrder.overall_price = overall_price
                finalOrder.orders.add(each)
                finalOrder.save()
            
            data['final_order'] = finalOrder.id
            return_data = {
                "trans_id": finalOrder.trans_id,
                "payment_method": data['payment_method']
            }
        except Exception:
            import traceback
            print(traceback.format_exc())
            pass

        #saving of data on dafault post request
        serializer = CustomerInfoSerializerPost(data=data) 
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        if not return_data:
            return_data = serializer.data
        return Response(return_data, status=status.HTTP_201_CREATED, headers=headers)
    

class TransactionView(viewsets.ModelViewSet):
    filter_fields = ('paid', 'final_order__overall_price', 'final_order__trans_id',)
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    lookup_field = 'final_order__trans_id'

    def get_permissions(self):
        if self.action in ['list', 'update']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]

        return [permission() for permission in permission_classes]

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer





    