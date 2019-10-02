from django.urls import path, include
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', AdminLanding.as_view(), name='admin_landing'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='login.html'), name='logout'),

    path('products', ProductListView.as_view(), name='admin_products'),
    path('update/product/<int:pk>', ProductUpdateView.as_view(), name='admin_product_update'),
    path('create/product/', ProductCreateView.as_view(), name='admin_product_create'),
    path('delete/product/<int:pk>', ProductDeleteView.as_view(), name='admin_product_delete'),

    path('customer_infos', CustomerInfoListView.as_view(), name='admin_customer_infos'),


]   
