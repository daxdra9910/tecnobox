from django.contrib import admin

from apps.utils.actions import BaseModelAdmin, disable_selected, enable_selected
from apps.accounts.models import City




@admin.register(City)
class CityAdmin(BaseModelAdmin):
    """
    Modelo City de la interfaz de administración.
    """
    list_display = ['name', 'region', 'created_at', 'updated_at', 'is_active']
    list_filter = ['region', 'is_active']
    search_fields = ['name', 'region']
    ordering = ['name', 'region']
    actions = [disable_selected, enable_selected]