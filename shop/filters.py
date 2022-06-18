from .models import Product
import django_filters


class ProductFilter(django_filters.FilterSet):

    class Meta:
        model = Product
        fields = ['name', 'title', 'weight', 'cost', 'created_at', 'type_medicine']
