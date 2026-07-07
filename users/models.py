from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=13, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} profile"
    