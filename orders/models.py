from django.db import models
from django.contrib.auth.models import User

from products.models import Product


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Awaiting Payment'),
        ('paid', 'Payment Received'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}-{self.status}-{self.total_price}"



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name}-total_sum-{self.quantity * self.price}"
    
    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.product.price

        super().save(*args, **kwargs)