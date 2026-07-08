from django.urls import path
from .views import ProductList

urlpatterns = [
    path('', ProductList.as_view(), name='home'),
    path('products/', ProductList.as_view(), name='product-list'),
]