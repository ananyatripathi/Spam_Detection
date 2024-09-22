from django.db import models
from django.conf import settings

class Spam(models.Model):
    phone_number = models.CharField(max_length=15)
    spam_count = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='reported_spam')

    def __str__(self):
        return f"{self.phone_number} - {self.spam_count}"
