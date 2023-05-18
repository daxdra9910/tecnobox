from django.contrib import admin

from apps.utils.actions import BaseModelAdmin, disable_selected, enable_selected
from apps.shop.models import Review




@admin.register(Review)
class ReviewAdmin(BaseModelAdmin):
    """
    Modelo Review de la interfaz de administración.
    """
    list_display = ['user', 'product', 'rating', 'comment', 'created_at', 'updated_at', 'is_active']
    search_fields = ['user', 'product', 'is_active']
    ordering = ['user', 'product', 'rating']
    actions = [disable_selected, enable_selected]