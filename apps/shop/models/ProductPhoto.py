from django.db import models
from django.utils.translation import gettext_lazy as _




class ProductPhoto(models.Model):
    """
    Información sobre las fotos de un producto específico.
    """
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE, related_name='photos', verbose_name=_('producto'))
    photo = models.ImageField(upload_to='products/', max_length=100, blank=True, verbose_name=_('foto'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('fecha de creación'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('fecha de actualización'))
    is_active = models.BooleanField(default=True, verbose_name=_('activo'))


    def __str__(self):
        return f'{self.product.name} photo'


    class Meta:
        verbose_name = _('foto de los productos')
        verbose_name_plural = _('fotos de los productos')