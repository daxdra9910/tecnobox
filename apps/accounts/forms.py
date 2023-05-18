from django.contrib.auth.forms import UserChangeForm

from apps.accounts.models import User




class UserChangeForm(UserChangeForm):
    """
    Formulario de modificación del modelo User.
    Define los campos que tendrá el formulario.
    """

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'birthdate', 'is_active', 'is_staff']