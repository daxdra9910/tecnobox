from django.contrib import admin

from apps.utils.actions import BaseModelAdmin, disable_selected, enable_selected
from apps.accounts.models import Region




@admin.register(Region)
class RegionAdmin(BaseModelAdmin):
    """
    Modelo Region de la interfaz de administración.
    """
    list_display = ['name', 'created_at', 'updated_at', 'is_active']
    search_fields = ['name', 'is_active']
    ordering = ['name']
    actions = [disable_selected, enable_selected]