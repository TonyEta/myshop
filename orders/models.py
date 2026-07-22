from django.db import models
from django.contrib.auth.models import User

from products.models import Product


class Order(models.Model):
    STATUS_CHOICES = (
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    PAYMENT_CHOICES = (
        ('cash', 'Cash on Delivery'),
        ('card', 'Credit/Debit Card')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='processing')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=30, choices=PAYMENT_CHOICES, default='cash')

    def __str__(self):
        return f"Order {self.pk} by {self.user}"



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('order', 'product')

    def __str__(self):
        return f"{self.product.name}-total_sum-{self.quantity * self.price}"
    
    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.product.price

        super().save(*args, **kwargs)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    session_key = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_cart_price(self):
        total_price = 0
        for item in self.cart_items.all():
            total_price += item.items_cost

        return total_price
    
    @property
    def total_cart_quantity(self):
        total_quantity = 0
        for item in self.cart_items.all():
            total_quantity += item.quantity

        return total_quantity
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()

    @property
    def items_cost(self):
        price = self.product.price * self.quantity

        return price