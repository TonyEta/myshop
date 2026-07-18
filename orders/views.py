import json

from django.shortcuts import render
from .models import Cart, CartItem
from products.models import Product


def action_with_cart(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        product_id = body.get('productId')
        user_action = body.get('action')
        target_item = Product.objects.get(id=product_id)

        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
        else:
            if request.session.session_key:
                cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
            else:
                request.session.create()
                cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=target_item)

        if user_action == 'add':
            
        elif user_action == 'remove':
            pass
        elif user_action == 'decrease':
            pass 
        elif user_action == 'increase':
            pass
        else:
            pass 
