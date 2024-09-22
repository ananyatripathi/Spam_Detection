from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'name', 'email', 'is_active', 'is_admin')
    search_fields = ('phone_number', 'name')
    list_filter = ('is_active', 'is_admin')
