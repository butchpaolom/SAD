import django_filters
from api_proc.models import Product

class ProductFilterSet(django_filters.FilterSet):
    sale_list = django_filters.BooleanFilter(method='get_sale', field_name='sale_list', label='Sale')
    

    def get_sale(self, queryset, field_name, value, ):
        print(value)
        if value:
            return Product.objects.all().exclude(sale=0).exclude(hidden=True)
        return queryset

    class Meta:
        model = Product
        fields = ['category__category_name', 'product_name', 'price', 'sale_list']