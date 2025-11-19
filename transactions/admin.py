from django.contrib import admin
from .models import Account

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'owner', 'balance', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('number', 'name', 'owner__username')
