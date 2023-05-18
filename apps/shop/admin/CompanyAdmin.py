from django.contrib import admin

from apps.utils.actions import BaseModelAdmin, disable_selected, enable_selected
from apps.shop.models import Company




@admin.register(Company)
class CompanyAdmin(BaseModelAdmin):
    """
    Modelo Company de la interfaz de administración.
    """
    list_display = ['name', 'address', 'phone', 'email', 'schedule', 'created_at', 'updated_at', 'is_active']
    search_fields = ['name', 'is_active']
    ordering = ['name']
    actions = [disable_selected, enable_selected]