from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.views import View




class ChangePassword(LoginRequiredMixin, View):
    """
    Cambia la contraseña del usuario autenticado.
    """
    login_url = reverse_lazy('accounts:signin')

    def get(self, request):
        """
        Muestra el formulario para cambiar la contraseña.
        """
        return render(request, 'accounts/profile/change_password.html')


    def post(self, request):
        """
        Cambia la contraseña del usuario.
        """
        # Obtenemos los datos del formulario.
        password = request.POST['password1']

        # Obtenemos el usuario autenticado.
        user = request.user

        # Validamos que el usuario no cambie la contraseña por la misma.
        if user.check_password(password):
            messages.error(request, 'La contraseña no puede ser la misma!')
            return redirect('accounts:change-password')

        # Actualizamos la contraseña del usuario en la base de datos.
        user.set_password(password)
        user.save()

        # Mostramos un mensaje indicando que el proceso ha sido exitoso.
        messages.success(
            request, 'Tu contraseña ha cambiado. Por favor inicia sesión de nuevo')

        # Redirigimos al usuario a la vista de login para que inicie sesión.
        return redirect('accounts:signin')