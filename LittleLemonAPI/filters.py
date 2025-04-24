from django_filters import rest_framework as filters
from .models import MenuItem, Order

class MenuItemFilter(filters.FilterSet):
    category_title = filters.CharFilter(field_name='category__title', lookup_expr='icontains')
    featured = filters.BooleanFilter()
    price = filters.NumberFilter()

    class Meta:
        model = MenuItem
        fields = ['price', 'featured', 'category_title']

class OrderFilter(filters.FilterSet):
    status = filters.BooleanFilter()
    date = filters.DateFilter()

    class Meta:
        model = Order
        fields = ['status', 'date']
