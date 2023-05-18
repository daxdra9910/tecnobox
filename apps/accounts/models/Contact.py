from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import City, Region, User




class Contact(models.Model):
    """
    Información de contacto de los usuarios de la aplicación.
    """
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, verbose_name=_('usuario'))
    region = models.ForeignKey('accounts.Region', on_delete=models.DO_NOTHING, verbose_name=_('departamento'))
    city = models.ForeignKey('accounts.City', on_delete=models.DO_NOTHING, verbose_name=_('ciudad'))
    address = models.CharField(max_length=75, verbose_name=_('dirección'))
    phone = models.CharField(max_length=10, verbose_name=_('teléfono'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('fecha de creación'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('fecha de actualización'))
    is_active = models.BooleanField(default=True, verbose_name=_('activo'))


    def __str__(self):
        return f'{self.user.username}\'s contact'


    class Meta:
        verbose_name = _('información de contacto')
        verbose_name_plural = _('informacion de contacto')