from django.contrib import admin

from apps.utils.actions import BaseModelAdmin, disable_selected, enable_selected
from apps.shop.models import ShoppingCart




@admin.register(ShoppingCart)
class ShoppingCartAdmin(BaseModelAdmin):
    """
    Modelo ShoppingCart de la interfaz de administración.
    """
    list_display = ['user', 'created_at', 'updated_at', 'is_active']
    list_filter = ['is_active']
    search_fields = ['user', 'is_active']
    ordering = ['user']
    actions = [disable_selected, enable_selected]