import json

from django.shortcuts import render
from django.http import JsonResponse
from .models import Cart, CartItem
from products.models import Product


def cart_view(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)

    return render(request, 'orders/cart.html', {'cart': cart})


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
            if not created and cart_item.quantity + 1 <= target_item.stock:
                cart_item.quantity += 1
                cart_item.save()
        elif user_action == 'remove':
            cart_item.delete()
        elif user_action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
        elif user_action == 'increase':
            if cart_item.quantity + 1 <= target_item.stock:
                cart_item.quantity += 1
                cart_item.save()

        if cart_item.pk:
            current_qty = cart_item.quantity
            current_costs = cart_item.items_cost
        else:
            current_qty = 0
            current_costs = 0

        return JsonResponse({
            'status': 'success',
            'cart_item_quantity': current_qty,
            'cart_item_costs': float(current_costs), 
            'cart_total_qty': cart.total_cart_quantity,
            'cart_total_price': float(cart.total_cart_price)
        })