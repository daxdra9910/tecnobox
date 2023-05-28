from django.contrib import admin

from apps.utils.actions import BaseModelAdmin, disable_selected, enable_selected
from apps.shop.models import ProductDiscount




@admin.register(ProductDiscount)
class ProductDiscountAdmin(BaseModelAdmin):
    """
    Modelo ProductDiscount de la interfaz de administración.
    """
    list_display = ['product', 'discount', 'formatted_value', 'created_at', 'is_active']
    readonly_fields = ['formatted_value']
    list_filter = ['is_active']
    search_fields = ['product', 'discount', 'is_active']
    ordering = ['product', 'discount']
    actions = [disable_selected, enable_selected]