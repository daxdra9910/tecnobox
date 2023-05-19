import secrets

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from PIL import Image




class User(AbstractUser):
    """
    Usuario de la aplicación. Al heredar de Abstract User, contiene
    los siguientes campos por defecto: username, password, email,
    first_name, last_name, is_active, is_staff, last_login, date_joined.
    """
    birthdate = models.DateField(null=True, blank=True, verbose_name=_('fecha de nacimiento'))
    password_reset_token = models.CharField(max_length=255, null=True, blank=True)
    password_reset_token_created_at = models.DateTimeField(null=True, blank=True)
    photo = models.ImageField(upload_to='profile/', max_length=100, blank=True, verbose_name=_('foto de perfil'))


    def __str__(self):
        return f'{self.username}'


    def generate_password_reset_token(self):
        """
        Crea un token para el restablecimiento de la contraseña.
        """
        token = secrets.token_urlsafe(32)
        self.password_reset_token = token
        self.password_reset_token_created_at = timezone.now()
        self.save()
        return token


    def get_url_photo(self):
        """
        Devuelve la URL de la foto de perfil del usuario. Si este no tiene,
        devuelve una imagen predefinida.
        """
        if self.photo:
            return self.photo.url
        else:
            return settings.MEDIA_URL + 'profile/default.jpg'


    def save(self, *args, **kwargs):
        """
        Se sobrescribe el método save() para que si el usuario sube una foto
        de un tamaño mayor a 200x200, se guarde con ese tamaño.
        """
        super().save(*args, **kwargs)
        if self.photo:
            img = Image.open(self.photo.path)
            if img.height > 200 or img.width > 200:
                output_size = (200, 200)
                img.thumbnail(output_size)
                img.save(self.photo.path)