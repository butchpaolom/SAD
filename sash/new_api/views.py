from django.shortcuts import render
from api_proc.models import *
from rest_framework import viewsets, permissions
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters
import django_filters
# Create your views here.

class ProductView(viewsets.ModelViewSet):
    search_fields = ['category__category_name', 'product_name']
    filter_fields = ['category', 'product_name']
    queryset = Product.objects.all()
    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# class CustomerInfoView

class CustomerInfoView(viewsets.ModelViewSet):
    queryset = CustomerInfo.objects.all()
    serializer_class = CustomerInfoSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]

        return [permission() for permission in permission_classes]

class TransactionView(viewsets.ModelViewSet):
    filter_fields = ('paid', 'final_order__overall_price', 'final_order__trans_id')
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action   in ['list', 'retrieve', 'update']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]

        return [permission() for permission in permission_classes]






    