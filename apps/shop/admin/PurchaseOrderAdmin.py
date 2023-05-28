import locale

from django.contrib import admin

from apps.utils.actions import BaseModelAdmin, disable_selected, enable_selected
from apps.shop.models import PurchaseOrder, ShoppingCart




@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(BaseModelAdmin):
    """
    Modelo PurchaseOrder de la interfaz de administración.
    """
    list_display = ['user', 'formatted_subtotal', 'formatted_taxes', 'formatted_total', 'payment_method', 'status', 'created_at']
    list_filter = ['status', 'is_active']
    readonly_fields = ['subtotal', 'taxes', 'total']
    search_fields = ['user', 'shopping_cart', 'payment_method', 'status', 'is_active']
    ordering = ['user', 'shopping_cart', 'payment_method', 'status']
    actions = [disable_selected, enable_selected]


    def formatted_subtotal(self, obj):
        locale.setlocale(locale.LC_ALL, '')
        number = locale.format('%d', obj.subtotal, grouping=True)
        return f'${number}'


    def formatted_taxes(self, obj):
        locale.setlocale(locale.LC_ALL, '')
        number = locale.format('%d', obj.taxes, grouping=True)
        return f'${number}'


    def formatted_total(self, obj):
        locale.setlocale(locale.LC_ALL, '')
        number = locale.format('%d', obj.total, grouping=True)
        return f'${number}'


    formatted_subtotal.short_description = 'Subtotal'
    formatted_taxes.short_description = 'Impuestos'
    formatted_total.short_description = 'Total'