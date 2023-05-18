from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html

from apps.utils.actions import BaseModelAdmin, disable_selected, enable_selected
from apps.accounts.forms import UserChangeForm
from apps.accounts.models import Contact, User




class ContactInline(admin.TabularInline):
    """
    Permite editar información de contacto en el formulario
    de creación/edición del modelo User.
    """
    model = Contact
    extra = 1




@admin.register(User)
class UserAdmin(BaseModelAdmin):
    """
    Modelo User de la interfaz de administración.
    """
    inlines = [ContactInline]
    form = UserChangeForm

    list_display = ['profile_photo', 'full_name', 'username', 'email', 'birthdate', 'date_joined', 'is_staff', 'is_active']
    list_filter = ['is_active', 'is_staff']
    search_fields = ['first_name', 'last_name', 'username', 'email']
    ordering = ['last_name', 'first_name', 'username']
    actions = [disable_selected, enable_selected]


    def profile_photo(self, obj):
        """
        Columna con la foto de perfil del usuario.
        """
        return format_html('<img src="{}" width="100" height="100" />'.format(obj.get_url_photo()))


    def full_name(self, obj):
        """
        Columna con el nombre completo del usuario.
        """
        return obj.get_full_name()


    profile_photo.short_description = 'Foto de perfil'
    full_name.short_description = 'Nombre completo'


    class Media:
        css = {
            'all': (settings.STATIC_URL + 'css/admin.css',)
        }