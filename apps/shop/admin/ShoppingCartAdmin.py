from django.contrib import admin

from apps.utils.actions import BaseModelAdmin, disable_selected, enable_selected
from apps.shop.models import ShoppingCart




@admin.register(ShoppingCart)
class ShoppingCartAdmin(BaseModelAdmin):
    """
    Modelo ShoppingCart de la interfaz de administración.
    """
    list_display = ['user', 'purchase_order', 'created_at', 'updated_at', 'is_active']
    search_fields = ['user', 'purchase_order', 'is_active']
    ordering = ['user', 'purchase_order']
    actions = [disable_selected, enable_selected]