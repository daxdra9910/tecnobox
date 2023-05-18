from django.contrib import admin

from apps.utils.actions import BaseModelAdmin, disable_selected, enable_selected
from apps.shop.models import ProductDiscount




@admin.register(ProductDiscount)
class ProductDiscountAdmin(BaseModelAdmin):
    """
    Modelo ProductDiscount de la interfaz de administración.
    """
    list_display = ['product', 'discount', 'discount_value', 'created_at', 'updated_at', 'is_active']
    search_fields = ['product', 'discount', 'discount_value', 'is_active']
    ordering = ['product', 'discount', 'discount_value']
    actions = [disable_selected, enable_selected]