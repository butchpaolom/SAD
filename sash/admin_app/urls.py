from django.urls import path, include
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', AdminDashboard.as_view(), name='admin_dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', logout_request, name='logout'),

    path('products', ProductListView.as_view(), name='admin_products'),
    path('update/product/<int:pk>', ProductUpdateView.as_view(), name='admin_product_update'),
    path('create/product/', ProductCreateView.as_view(), name='admin_product_create'),
    path('delete/product/<int:pk>', ProductDeleteView.as_view(), name='admin_product_delete'),
    path('reprice/product/', ProductRepriceView.as_view(), name='admin_product_reprice'),

    path('customer_infos', CustomerInfoListView.as_view(), name='admin_customer_infos'),

    path('transactions', TransactionListView.as_view(), name='admin_transactions'),
    path('transactions/delivery/<int:pk>', TransactionDeliveryDateSet.as_view(), name='admin_delivery_date_set'),
    path('transactions/delivered/<int:pk>', TransactionDeliveredDateSet.as_view(), name='admin_delivered_date_set'),

    path('final_order/<int:pk>', FinalOrderDetailView.as_view(), name='admin_final_order_detail'),

    path('transactions/cod/<int:pk>', CashOnDeliveryUpdate.as_view(), name='admin_cash_on_delivery_update'),
    #components dashboard
    path('sales_chart', sales_chart, name='admin_sales_chart'),
    path('most_viewed', most_viewed, name='admin_most_viewed'),
    path('total_transactions', total_transactions, name='admin_total_transactions'),
    path('total_earnings', total_earnings, name='admin_total_earnings'),
    path('be_delivered', be_delivered, name='admin_be_delivered'),
    path('least_stock', least_stock, name='admin_least_stock'),


    path('update/customer_name/<int:pk>', CustomerInfoNameUpdateView.as_view(), name='admin_customer_name_update'),
    path('update/customer_address/<int:pk>', CustomerInfoAddressUpdateView.as_view(), name='admin_customer_address_update'),
    
    path('update/front_assets/<int:pk>', UpdateAssets.as_view(), name='admin_update_front_assets'),

    path('bulk', bulk_upload, name='admin_bulk_upload')
]   
