from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import Q, Avg

from .models import Product


class ProductListView(ListView):
    model = Product
    template_name = 'products/home-products-list.html'
    context_object_name = 'products'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True).prefetch_related('specifications')

        category = self.request.GET.get('category')
        price_min = self.request.GET.get('price_min')
        price_max = self.request.GET.get('price_max')
        search = self.request.GET.get('search')
        sort = self.request.GET.get('sort')

        if sort == 'rating':
            queryset = queryset.annotate(rating=Avg('reviews__rating'))
            sort = '-rating'
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

class ProductDetailView(DetailView):
    model = Product
    template_name= 'products/product-detail.html'
    context_object_name = 'product'