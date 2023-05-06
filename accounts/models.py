import secrets

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils import timezone




class Region(models.Model):
    """
    Departamentos de Colombia.
    """
    regions = models.Manager()

    name = models.CharField(max_length=75)


    def __str__(self):
        return f'{self.name}'




class City(models.Model):
    """
    Ciudades de Colombia.
    """
    cities = models.Manager()

    name = models.CharField(max_length=75)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.name}'




class User(AbstractUser):
    """
    Usuario de la aplicación. Al heredar de Abstract User, contiene
    los siguientes campos por defecto: username, password, email,
    first_name, last_name, is_active, is_staff, last_login, date_joined.
    """
    users = UserManager()

    birthdate = models.DateField(null=True, blank=True)
    password_reset_token = models.CharField(max_length=255, null=True, blank=True)
    password_reset_token_created_at = models.DateTimeField(null=True, blank=True)

    photo = models.ImageField(upload_to='images/', max_length=100, blank=True, )


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




class Contact(models.Model):
    """
    Información de contacto de los usuarios de la aplicación.
    """
    contacts = models.Manager()

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.DO_NOTHING)
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING)
    address = models.CharField(max_length=75)
    phone = models.CharField(max_length=10)


    def __str__(self):
        return f'{self.user.username}\'s contact'