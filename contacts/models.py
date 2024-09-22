from django.db import models
from django.conf import settings

class Contact(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contacts')
    phone_number = models.CharField(max_length=15)
    name = models.CharField(max_length=255)

    class Meta:
        unique_together = ('user', 'phone_number')

    def __str__(self):
        return f"{self.name} ({self.phone_number})"
