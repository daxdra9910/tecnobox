from django.contrib import admin

from apps.utils.actions import BaseModelAdmin, disable_selected, enable_selected
from apps.shop.models import PaymentMethod




@admin.register(PaymentMethod)
class PaymentMethodAdmin(BaseModelAdmin):
    """
    Modelo PayMethod de la interfaz de administración.
    """
    list_display = ['name', 'created_at', 'updated_at', 'is_active']
    search_fields = ['name', 'is_active']
    ordering = ['name']
    actions = [disable_selected, enable_selected]