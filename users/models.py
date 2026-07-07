from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.
    date_of_birth = models.DateField()
    address = models.TextField()

    def __str__(self):
        return f"{self.user.username} profile"