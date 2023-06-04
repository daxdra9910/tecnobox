from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _




class AdminstoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.adminstore'
    verbose_name = _('Panel de administración')
