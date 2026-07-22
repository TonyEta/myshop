from django.shortcuts import redirect, get_object_or_404

from .models import Cart, CartItem
from products.models import Product


def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)

    return cart

def action_with_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')
        next = request.POST.get('next')

        cart = get_or_create_cart(request)
        product = get_object_or_404(Product, pk=product_id)
        cart_item, _ = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 1})

        if action == 'increase' and product.stock > cart_item.quantity:
            cart_item.quantity += 1
            cart_item.save()

        elif action == 'decrease' and cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()

        elif action == 'decrease' and cart_item.quantity == 1:
            cart_item.delete()

        return redirect(next)