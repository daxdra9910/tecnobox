from django.contrib import admin
from django.utils.html import format_html

from apps.utils.actions import BaseModelAdmin, disable_selected, enable_selected
from apps.shop.models import ProductPhoto




@admin.register(ProductPhoto)
class ProductPhotoAdmin(BaseModelAdmin):
    """
    Modelo ProductPhoto de la interfaz de administración.
    """
    list_display = ['product', 'image', 'created_at', 'updated_at', 'is_active']
    search_fields = ['product', 'is_active']
    ordering = ['product']
    actions = [disable_selected, enable_selected]


    def image(self, obj):
        """
        Columna con la foto del producto.
        """
        return format_html('<img src="{}" width="100" height="100" />'.format(obj.photo.url))


    image.short_description = 'Imagen'