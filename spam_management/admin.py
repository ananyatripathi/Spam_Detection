# spam/admin.py
from django.contrib import admin
from .models import Spam

class SpamAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'spam_count')

    def spam_count(self, obj):
        return Spam.objects.filter(phone_number=obj.phone_number).count()
    spam_count.short_description = 'Spam Count'

admin.site.register(Spam, SpamAdmin)
