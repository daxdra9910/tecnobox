from django.contrib import admin




class BaseModelAdmin(admin.ModelAdmin):
    """
    Clase base que remueve la acción predefinida "delete_selected".
    """

    def get_actions(self, request):
        """
        Quitamos la acción "eliminar seleccionados".
        """
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions




@admin.action(description='Eliminar seleccionado/s')
def disable_selected(model_admin, request, queryset):
    """
    Acción de soft deleting.
    """
    # Desactivamos los elementos seleccionados.
    queryset.update(is_active=False)

    # Mostramos un mensaje de éxito
    model_admin.message_user(request, "Los elementos seleccionados fueron eliminados correctamente.")




@admin.action(description='Habilitar seleccionado/s')
def enable_selected(model_admin, request, queryset):
    """
    Acción opuesta al soft deleting.
    """
    # Activamos los elementos seleccionados.
    queryset.update(is_active=True)

    # Mostramos un mensaje de éxito
    model_admin.message_user(request, "Los elementos seleccionados fueron habilitados correctamente.")
