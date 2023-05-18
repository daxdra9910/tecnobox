from django.db import models
from django.utils.translation import gettext_lazy as _




class Company(models.Model):
    """
    Información de la tienda virtual.
    """
    name = models.CharField(max_length=75, verbose_name=_('nombre'))
    address = models.CharField(max_length=100, verbose_name=_('dirección'))
    phone = models.CharField(max_length=10, verbose_name=_('teléfono'))
    email = models.EmailField(max_length=75, verbose_name=_('email'))
    schedule = models.TextField(max_length=150, verbose_name=_('horario'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('fecha de creación'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('fecha de actualización'))
    is_active = models.BooleanField(default=True, verbose_name=_('activo'))


    def __str__(self):
        return f'{self.name}'


    class Meta:
        verbose_name = _('empresa')
        verbose_name_plural = _('empresas')