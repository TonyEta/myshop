from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import Q, Avg

from .models import Product
from orders.models import CartItem
from tools import get_or_create_cart

class ProductListView(ListView):
    model = Product
    template_name = 'products/home-products-list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True).prefetch_related('specifications')

        categories = self.request.GET.getlist('category')
        price_min = self.request.GET.get('price_min')
        price_max = self.request.GET.get('price_max')
        search = self.request.GET.get('search')
        sort = self.request.GET.get('sort')

        
        if sort == 'rating':
            queryset = queryset.annotate(rating=Avg('reviews__rating'))
            sort = '-rating'
        if categories:
            queryset = queryset.filter(category__name__in=categories)
        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)
        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(description__icontains=search))
        if sort:
            queryset = queryset.order_by(sort)
        

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_params = self.request.GET.copy()

        if 'page' in query_params:
            del query_params['page']
        
        context['query_string'] = query_params.urlencode()
        
        context['query_sort'] = self.request.GET.get('sort', 'created_at')
        context['query_search'] = self.request.GET.get('search', '')
        context['query_categories'] = self.request.GET.getlist('category')

        return context
    
class ProductDetailView(DetailView):
    model = Product
    template_name= 'products/product-detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_or_create_cart(self.request)
        cart_item = CartItem.objects.filter(Q(cart=cart) & Q(product=self.object)).first()
        context['cart_item'] = cart_item

        return context