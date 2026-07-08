from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Q

from .models import Product


class ProductList(ListView):
    model = Product
    template_name = 'products/home-products-list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()

        category = self.request.GET.get('category')
        price_min = self.request.GET.get('price_min')
        price_max = self.request.GET.get('price_max')
        search = self.request.GET.get('search')
        sort = self.request.GET.get('sort')

        if category:
            queryset = queryset.filter(category__name=category)
        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)
        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(description__icontains=search))
        if sort:
            queryset = queryset.order_by(sort)

        return queryset
