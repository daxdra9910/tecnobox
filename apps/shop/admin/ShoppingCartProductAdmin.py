from django.contrib import admin

from apps.utils.actions import BaseModelAdmin, disable_selected, enable_selected
from apps.shop.models import ShoppingCartProduct




@admin.register(ShoppingCartProduct)
class ShoppingCartProductAdmin(BaseModelAdmin):
    """
    Modelo ShoppingCartProduct de la interfaz de administración.
    """
    list_display = ['product', 'cart', 'amount', 'created_at', 'updated_at', 'is_active']
    search_fields = ['product', 'cart', 'is_active']
    ordering = ['product', 'cart']
    actions = [disable_selected, enable_selected]