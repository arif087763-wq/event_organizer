from django.contrib import admin
from .models import Payment

admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('registration', 'amount', 'method', 'is_confirmed', 'created_at')
    list_filter = ('method', 'is_confirmed', 'created_at')
    search_fields = ('registration__registration_code', 'registration__participant__username')
    readonly_fields = ('created_at', 'confirmed_at')