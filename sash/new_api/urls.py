from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('api_products', views.ProductView)
router.register('api_category', views.CategoryView)
router.register('api_customer_info', views.CustomerInfoView)
router.register('api_transaction', views.TransactionView)

urlpatterns = [
    path('', include(router.urls))
    ]   
