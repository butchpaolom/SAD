import django_filters
from api_proc.models import Product
from rest_framework.filters import OrderingFilter
from django.db.models import F,Q

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


class ProductOrder(OrderingFilter):
    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)

        if ordering == ['price']:
            return queryset.order_by(F('price')*(1-(F('sale')*0.01)))
        elif ordering == ['-price']:
            return queryset.order_by(F('price')*(1-(F('sale')*0.01))).reverse()
        elif ordering:
            return queryset.order_by(*ordering)

        return queryset