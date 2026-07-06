from django.db import models
from django.contrib.auth.models import User


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
    updatet_at = models.DateTimeFiedl(auto_now=True)

    def __str__(self):
        return f"{self.user}-{self.status}-{self.total_price}"
