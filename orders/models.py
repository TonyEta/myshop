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

    def __str__(self):
        return f"{self.product.name}-total_sum-{self.quantity * self.price}"
    
    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.product.price

        super().save(*args, **kwargs)