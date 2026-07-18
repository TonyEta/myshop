from django.urls import path
from .views import action_with_cart


urlpatterns = [
    path('cart/update_item/', action_with_cart, name='action-with-cart'),