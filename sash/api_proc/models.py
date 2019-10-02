from django.db import models
from PIL import Image
import uuid

# Create your models here.

#category
class Category(models.Model):
    category_name = models.CharField(max_length=30)

    def __str__(self):
        return str(self.category_name)

#default Product table
class Product(models.Model):
    product_name = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    product_image = models.ImageField(null=True)
    description = models.TextField()
    price = models.DecimalField(null=True, decimal_places=2, max_digits=8)
    stock = models.IntegerField(null=True)

    def __str__(self):
        return str(self.product_name)

    def category_name(self):
        return str(self.category.category_name)

    def in_stock(self):
        if self.stock != 0:
            return True
        else:
            return False

#Initial Order with quantity
class InitialOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)
    total_price = models.DecimalField(null=True, blank=False, decimal_places=2, max_digits=8)

    def __str__(self):
        return '{0}-{1}'.format(self.product, self.quantity)

#Final Order (Multiple Initial Order)
class FinalOrder(models.Model):
    orders = models.ManyToManyField(InitialOrder)
    overall_price = models.DecimalField(null=True, default=0, decimal_places=2, max_digits=8)

    def __str__(self):
        return '{0}-{1}'.format(self.overall_price, self.id)

#Customer info + Final Order
class CustomerInfo(models.Model):
    final_order = models.ForeignKey(FinalOrder, on_delete=models.CASCADE)
    address = models.TextField(blank=False, null=False)
    first_name = models.CharField(max_length=30, null=True, blank=False)
    last_name = models.CharField(max_length=30, null=True, blank=False)
    middle_initial = models.CharField(max_length=3, null=True, blank=True)
    contact_number = models.TextField()

    def __str__(self):
        return '{0}-{1} {2}'.format(self.final_order.pk, self.first_name, self.last_name)

class Transaction(models.Model):
    costumer = models.ForeignKey(CustomerInfo, on_delete=models.CASCADE)
    trans_id = models.UUIDField(default=uuid.uuid4, editable=False)
    delivery_date = models.DateTimeField()
    delivered_date = models.DateTimeField()

    def __str__(self):
        return '{0} {1} - {2}'.format(self.costumer.first_name, self.costumer.last_name, self.trans_id)

    