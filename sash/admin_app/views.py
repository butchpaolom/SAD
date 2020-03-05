from django.shortcuts import render, redirect
from front_ep.models import *
from api_proc.models import *
import requests
from django.views.generic import ListView, TemplateView, UpdateView, CreateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from bootstrap_modal_forms.mixins import PassRequestMixin
from django.contrib.messages.views import SuccessMessageMixin
from .forms import *
from django.contrib import messages
import datetime
from django.http import JsonResponse
from django.db.models import Sum
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
import xlrd
from django.contrib import messages

import threading



def update_delivery_email(data):
    customer = CustomerInfo.objects.get(final_order__id=data.final_order.id)
    name = customer.first_name
    email = customer.email
    address = customer.address
    print(email)
    subject = 'Delivery update!'
    html_message = render_to_string('email/deliver_email.html', {
        'name': name,
        'address': address,
        'delivery_date': data.delivery_date,
        'trans_id': data.final_order.trans_id
        })
    plain_message = strip_tags(html_message)
    from_email = 'realtantan7@gmail.com'
    to = email

    mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

# Create your views here.

def logout_request(request):
    logout(request)
    return redirect('login')
    
class AdminLanding(LoginRequiredMixin, TemplateView):
    template_name = 'admin_base.html'

class AdminDashboard(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

#Product
class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'product_tables.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        try:
            search = self.request.GET['id']
        except:
            search = ""
        context = super().get_context_data(**kwargs)  
        context['search'] = search
        return context


class ProductUpdateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Product
    template_name = 'update.html'
    success_url = reverse_lazy('admin_products')
    form_class = ProductEditForm
    
    def get_success_message(self, cleaned_data):
        product_name = Product.objects.get(id=self.kwargs.get('pk'))
        message = "Successfully updated " + str(product_name)
        return message

    def form_valid(self, form):
        self.object = form.save(commit=False)
        old_list = Product.objects.filter(product_name=self.object.product_name).exclude(id=self.object.id)
        for each in old_list:
            each.hidden = True
            each.views = self.object.views
            each.stock = self.object.stock
            each.save()
        if old_list:
            self.object.hidden=False
        self.object.save()
        return super(ProductUpdateView, self).form_valid(form)


class ProductCreateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'create.html'
    form_class = ProductForm
    context_object_name = 'product'
    success_url = reverse_lazy('admin_products')

    def get_success_message(self, cleaned_data):
        message = "Successfully added " + str(self.object.product_name)
        return message 

    def form_valid(self, form):
        self.object = form.save(commit=False)
        old_list = Product.objects.filter(product_name=self.object.product_name).exclude(id=self.object.id)
        for each in old_list:
            each.hidden = True
            each.views = self.views
            each.stock = self.stock
            each.save()
        if old_list:
            self.object.hidden=False
        self.object.save()
        return super(ProductCreateView, self).form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, message=form.errors, extra_tags='danger')
        return redirect('admin_products')

class ProductRepriceView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'reprice.html'
    form_class = ProductRepriceForm
    context_object_name = 'product'
    success_url = reverse_lazy('admin_products')

    def get_success_message(self, cleaned_data):
        message = "Successfully repriced " + str(self.object.product_name)
        return message 

    def form_valid(self, form):
        self.object = form.save(commit=False)
        old_list = Product.objects.filter(product_name=self.object.product_name).exclude(id=self.object.id)
        for each in old_list:
            each.hidden = True
            each.save()
        old = old_list.first()
        self.object.category = old.category
        self.object.product_image = old.product_image
        self.object.product_image1 = old.product_image1
        self.object.product_image2 = old.product_image2
        self.object.description = old.description
        self.object.stock = old.stock
        self.object.views = old.views
        self.object.hidden=False
        self.object.save()
        return super(ProductRepriceView, self).form_valid(form)
    

class ProductDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Product
    context_object_name = 'product'
    success_url = reverse_lazy('admin_products')
    template_name = 'delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        context['model'] = self.model.__name__
        context['name'] = Product.objects.get(id=self.kwargs.get('pk')).product_name
        return context

    def delete(self, request, *args, **kwargs):
        product_name = Product.objects.get(id=self.kwargs.get('pk'))
        message = "Successfully deleted " + str(product_name)
        messages.warning(self.request, message)
        return super(ProductDeleteView, self).delete(request, *args, **kwargs)


#CustomerInfo
class CustomerInfoNameUpdateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = CustomerInfo
    template_name = 'update.html'
    success_url = reverse_lazy('admin_customer_infos')
    form_class = CustomerInfoNameUpdate

    def get_success_message(self, cleaned_data):
        customer = CustomerInfo.objects.get(id=self.kwargs.get('pk'))
        message = "Successfully updated " + "{0} {1}".format(str(customer.first_name), str(customer.last_name))
        return message

class CustomerInfoAddressUpdateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = CustomerInfo
    template_name = 'update.html'
    success_url = reverse_lazy('admin_customer_infos')
    form_class = CustomerInfoAddressUpdate

    def get_success_message(self, cleaned_data):
        customer = CustomerInfo.objects.get(id=self.kwargs.get('pk'))
        message = "Successfully updated " + "{0} {1}".format(str(customer.first_name), str(customer.last_name)) + " address to " + str(customer.address)
        return message

class CustomerInfoListView(LoginRequiredMixin, ListView):
    model = CustomerInfo
    template_name = 'customer_info_tables.html'
    context_object_name = 'customer_infos'

#Transaction
class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'transaction_tables.html'
    context_object_name = 'transactions'

    def get_context_data(self, **kwargs):
        try:
            search = self.request.GET['id']
        except:
            search = ""
        context = super().get_context_data(**kwargs)  
        context['search'] = search
        context['customer_infos'] = CustomerInfo.objects.all()
        return context




class TransactionDeliveryDateSet(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Transaction
    template_name = 'update.html'
    success_url = reverse_lazy('admin_transactions')
    form_class = TransactionDeliveryDateForm
    
    def form_valid(self, form):
        if self.object.delivery_date and not self.object.paid and not self.object.delivered_date:
            self.object.status = 1
        elif self.object.delivered_date and self.object.paid and not self.object.delivered_date:
            self.object.status = 2
        else:
            self.object.status = 3
        self.object = form.save()
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        transaction = Transaction.objects.get(id=self.kwargs.get('pk'))
        trans_id = transaction.final_order.trans_id
        thread_list = []
        thread = threading.Thread(target=update_delivery_email, args=(transaction,))
        thread_list.append(thread)
        thread.start()
        message = "Successfully updated " + str(trans_id)
        return message


class TransactionDeliveredDateSet(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Transaction
    template_name = 'update.html'
    success_url = reverse_lazy('admin_transactions')
    form_class = TransactionDeliveredDateForm

    def get_success_message(self, cleaned_data):
        transaction = Transaction.objects.get(id=self.kwargs.get('pk'))
        trans_id = transaction.final_order.trans_id
        print(self.object.final_order.trans_id)
        message = "Successfully updated " + str(trans_id)
        return message

    def form_valid(self, form):
        if self.object.delivery_date and not self.object.paid and not self.object.delivered_date:
            self.object.status = 1
        elif self.object.delivered_date and self.object.paid and not self.object.delivered_date:
            self.object.status = 2
        else:
            self.object.status = 3
        self.object = form.save()
        return super().form_valid(form)



#FinalOrderView
class FinalOrderDetailView(LoginRequiredMixin, DetailView):
    model = FinalOrder
    template_name = 'final_order_detail.html'
    context_object_name = 'final_order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        context['customer_info'] = CustomerInfo.objects.get(final_order=self.object)
        return context


#CODUpdate
class CashOnDeliveryUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Transaction
    template_name = 'update.html'
    success_url = reverse_lazy('admin_transactions')
    form_class = CashOnDeliveryUpdate

    def form_valid(self, form):
        if self.object.delivery_date and not self.object.paid and not self.object.delivered_date:
            self.object.status = 1
        elif self.object.delivery_date and self.object.paid and not self.object.delivered_date:
            self.object.status = 2
        else:
            self.object.status = 3
        print(self.object)
        self.object = form.save()
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        trans_id = Transaction.objects.get(id=self.kwargs.get('pk')).final_order.trans_id
        message = "Successfully updated " + str(trans_id)
        return message

#Assets
class UpdateAssets(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = FrontAsset
    fields = '__all__'
    template_name = 'update.html'
    success_url = reverse_lazy('admin_dashboard')

    def get_success_message(self, cleaned_data):
        message = "Successfully updated."
        return message

#DASHBOARD CHARTS
@login_required
def sales_chart(request):
    date_now = datetime.datetime.now()
    month = date_now.month
    year = date_now.year
    today = datetime.date.today()
    first = today.replace(day=1)
    last_month = first - datetime.timedelta(days=1)
    transactions = Transaction.objects.filter(delivered_date__year=year).filter(delivered_date__month=month).filter(paid=True)
    transactions1 = Transaction.objects.filter(delivered_date__year=year).filter(delivered_date__month=month-1).filter(paid=True)
    earned_money_current = [0] * 31
    earned_money_previous = [0] * 31
    for transaction in transactions:
        day = transaction.delivered_date.day
        earned_money_current[day-1] = earned_money_current[day-1] + float(transaction.final_order.overall_price)

    for transaction in transactions1:
        day = transaction.delivered_date.day
        earned_money_previous[day-1] = earned_money_previous[day-1] + float(transaction.final_order.overall_price)
    
    context = {
        "earned_current": earned_money_current,
        "current_month": date_now.strftime("%B"),
        "earned_previous": earned_money_previous,
        "previous_month": last_month.strftime("%B")
    }


    return render(request, 'dashboard_components/sales_chart.html', context)

@login_required
def most_viewed(request):
    product = Product.objects.all().order_by('views').last()

    context = {
        "product_name": product.product_name,
        "views": product.views
    }

    return render(request, 'dashboard_components/most_viewed.html', context)

@login_required
def total_transactions(request):
    date_now = datetime.datetime.now()
    month = date_now.month
    year = date_now.year
    transactions = Transaction.objects.filter(paid=True).filter(delivered_date__year=year).filter(delivered_date__month=month)

    context = {
        "total_transactions": len(transactions)
    }

    return render(request, 'dashboard_components/total_transactions.html', context)

@login_required
def total_earnings(request):
    date_now = datetime.datetime.now()
    month = date_now.month
    year = date_now.year
    transactions = Transaction.objects.filter(paid=True).filter(delivered_date__year=year).filter(delivered_date__month=month).aggregate(Sum('final_order__overall_price'))
    print(transactions)
    if transactions['final_order__overall_price__sum'] == None:
        transactions['final_order__overall_price__sum'] = 0
    context = {
        "total_earnings": "{:0,.2f}".format(float(transactions['final_order__overall_price__sum']))
    }
    
    return render(request, 'dashboard_components/total_earnings.html', context)

@login_required
def be_delivered(request):
    date_now = datetime.datetime.now()
    month = date_now.month
    year = date_now.year
    transactions = Transaction.objects.filter(delivery_date__isnull=False).filter(delivered_date__isnull=True).filter(delivery_date__year=year).filter(delivery_date__month=month)
    print(transactions)
    context = {
        "be_delivered": len(transactions)
    }
    
    return render(request, 'dashboard_components/be_delivered.html', context)

@login_required
def least_stock(request):
    products = Product.objects.all().order_by('stock')

    context = {
        "products": products
    }

    return render(request, 'dashboard_components/least_stock.html', context)


#bulk
@login_required
def bulk_upload(request):
    if request.method == 'GET':
        return render(request, 'fileuploads.html')
    if request.method == 'POST':
        try:
            uploaded_images = request.FILES.getlist('images')
            array_print(uploaded_images)

            for image in uploaded_images:
                f = FileSystemStorage()
                f.save(image.name, image)

            xl = request.FILES['infos']
            xlf = FileSystemStorage()
            xlf.save(xl.name, xl)

            wb = xlrd.open_workbook(xlf.path(xl.name)) 
            sheet = wb.sheet_by_index(0)
            print(sheet)
            for row in range(1,sheet.nrows):
                product_name = sheet.cell_value(row, 0)
                image = sheet.cell_value(row, 1)
                category = sheet.cell_value(row, 2)
                description = sheet.cell_value(row, 3)
                price = sheet.cell_value(row, 4)
                stock = sheet.cell_value(row, 5)
                delivery = sheet.cell_value(row, 6)
                hidden = sheet.cell_value(row, 7)

                print(f"{product_name} {image} {category} {description} {price} {stock} {delivery} {hidden}")
                product = Product(
                                product_name=product_name,
                                product_image=image,
                                category = Category.objects.get(category_name__icontains=category),
                                description = description,
                                price = price,
                                stock = stock,
                                hidden = hidden,
                                delivery_price=delivery,
                                )
                product.save()

            
            messages.success(request, 'Products Successfully Added!')


            return redirect('admin_products')
        except Exception as e:
            print(e)
            messages.error(request, str(e), extra_tags='danger')
            return redirect('admin_products')


def array_print(array):
    for each in array:
        print(each)


    

