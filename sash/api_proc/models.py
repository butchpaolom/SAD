from django.db import models
from PIL import Image
import uuid
from django.utils import timezone

# Create your models here.

def capitalize(string):
            string = ' '.join([each.capitalize() for each in string.lower().split()])
            return string
#category
class Category(models.Model):
    category_name = models.CharField(max_length=30)
    image = models.ImageField(null=True, blank=False)
    def __str__(self):
        return str(self.category_name)

#default Product table
class Product(models.Model):
    product_name = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    product_image = models.ImageField(null=True, blank=False)
    product_image1 = models.ImageField(null=True, blank=True)
    product_image2 = models.ImageField(null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(null=True, decimal_places=2, max_digits=8)
    stock = models.IntegerField(null=True)
    delivery_price = models.DecimalField(null=True, blank=False, decimal_places=2, max_digits=8)
    views = models.PositiveIntegerField(null=True)

    def in_stock(self):
        return str(self.stock > 0)

    def __str__(self):
        return str(self.product_name)

    def category_name(self):
        return str(self.category.category_name)


#Initial Order with quantity
#no login required
class InitialOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)
    total_price = models.DecimalField(null=True, blank=False, decimal_places=2, max_digits=8)

    def __str__(self):
        return '{0}-{1}'.format(self.product, self.quantity)

#Final Order (Multiple Initial Order)
#no login required
class FinalOrder(models.Model):
    orders = models.ManyToManyField(InitialOrder)
    overall_price = models.DecimalField(null=True, default=0, decimal_places=2, max_digits=8)
    trans_id = models.UUIDField(default=uuid.uuid4, editable=False)
    def __str__(self):
        return '{0}-{1}'.format(self.overall_price, self.trans_id)

#Customer info + Final Order
#no login required
class CustomerInfo(models.Model):
    final_order = models.ForeignKey(FinalOrder, on_delete=models.CASCADE)
    address = models.TextField(blank=False, null=False)
    first_name = models.CharField(max_length=30, null=True, blank=False)
    last_name = models.CharField(max_length=30, null=True, blank=False)
    middle_initial = models.CharField(max_length=3, null=True, blank=True)
    contact_number = models.TextField(blank=False)
    email = models.EmailField(blank=False, null=True)
    date_ordered = models.DateTimeField(editable=False, default=timezone.now)

    choices = (
        (1, "COD"),
        (2, "PayPal")
    )
    payment_method = models.IntegerField(choices, null=True)

    def save(self, *args, **kwargs):
        self.first_name = capitalize(self.first_name)
        self.last_name = capitalize(self.last_name)
        if self.middle_initial:
            self.middle_initial = capitalize(self.middle_initial)
        super(CustomerInfo, self).save(*args, **kwargs)

        
    def __str__(self):
        return '{0}-{1} {2}'.format(self.final_order.pk, self.first_name, self.last_name)

class Transaction(models.Model):
    final_order = models.OneToOneField(FinalOrder, on_delete=models.CASCADE, null=True)
    paid = models.BooleanField(default=0)
    delivery_date = models.DateTimeField(null=True)
    delivered_date = models.DateTimeField(null=True)

    def __str__(self):
        return '{0}'.format(self.final_order)


    