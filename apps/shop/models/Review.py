from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _




class Review(models.Model):
    """
    Información acerca de las reseñas hechas sobre un producto.
    """
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, verbose_name=_('cliente'))
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE, related_name='reviews', verbose_name=_('producto'))
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], verbose_name=_('puntaje'))
    comment = models.TextField(verbose_name=_('comentario'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('fecha de creación'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('fecha de actualización'))
    is_active = models.BooleanField(default=True, verbose_name=_('activo'))


    def __str__(self):
        return f'{self.product.name} ({self.rating}/5 by {self.user.username})'


    class Meta:
        verbose_name = _('reseña')
        verbose_name_plural = _('reseñas')