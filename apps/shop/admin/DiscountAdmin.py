from django.contrib import admin

from apps.utils.actions import BaseModelAdmin, disable_selected, enable_selected
from apps.shop.models import Discount




@admin.register(Discount)
class DiscountAdmin(BaseModelAdmin):
    """
    Modelo Discount de la interfaz de administración.
    """
    list_display = ['name', 'percentage', 'finish_at', 'created_at', 'updated_at', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'percentage', 'finish_at', 'is_active']
    ordering = ['name', 'percentage', 'finish_at']
    actions = [disable_selected, enable_selected]