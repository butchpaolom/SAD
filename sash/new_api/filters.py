import django_filters
from api_proc.models import Product

class ProductFilterSet(django_filters.FilterSet):
    sale_list = django_filters.filters.BooleanFilter(field_name='sale', method='get_sale')



    class Meta:
        model = Product
        fields = ['category__category_name', 'product_name', 'price', 'sale_list']

    def get_sale(self, queryset, name, value):
        print(value)
        if value:
            return queryset.exclude(sale=0)
        else:
            return queryset


