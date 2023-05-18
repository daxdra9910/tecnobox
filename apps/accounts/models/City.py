from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import Region




class City(models.Model):
    """
    Ciudades de Colombia.
    """
    name = models.CharField(max_length=75, verbose_name=_('nombre'))
    region = models.ForeignKey('accounts.Region', on_delete=models.CASCADE, verbose_name=_('departamento'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('fecha de creación'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('fecha de actualización'))
    is_active = models.BooleanField(default=True, verbose_name=_('activo'))


    def __str__(self):
        return f'{self.name}'


    class Meta:
        verbose_name = _('ciudad')
        verbose_name_plural = _('ciudades')