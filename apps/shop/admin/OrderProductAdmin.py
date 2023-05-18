from django.contrib import admin

from apps.utils.actions import BaseModelAdmin, disable_selected, enable_selected
from apps.shop.models import OrderProduct




@admin.register(OrderProduct)
class OrderProductAdmin(BaseModelAdmin):
    """
    Modelo OrderProduct de la interfaz de administración.
    """
    list_display = ['product', 'order', 'amount', 'created_at', 'updated_at', 'is_active']
    search_fields = ['product', 'order', 'is_active']
    ordering = ['product', 'order', 'amount']
    actions = [disable_selected, enable_selected]