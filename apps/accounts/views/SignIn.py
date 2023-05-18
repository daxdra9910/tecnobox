from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.views import View




class SignIn(View):
    """
    Inicio de sesión.
    """

    def get(self, request):
        """
        Muestra el formulario para iniciar sesión.
        """
        return render(request, 'accounts/signin.html')


    def post(self, request):
        """
        Valida las credenciales para el inicio de sesión.
        """
        # Obtenemos los datos del formulario.
        username = request.POST['username']
        password = request.POST['password']
        remember_me = request.POST.get('remember-me', False)

        # Buscamos un usuario con esas credenciales.
        user = authenticate(username=username, password=password)

        # Si el usuario existe, lo redirigimos al home.
        if user:
            login(request, user)

            # Si se ha marcado la casilla Recuérdame, guarda la sesión por 30 días.
            if remember_me:
                request.session.set_expiry(30)
                response = redirect('shop:home')
                response.set_cookie('remember_me', user.pk, max_age=30)
                return response

            return redirect('shop:home')

        # Si el usuario no existe, mostramos el formulario con un mensaje de error.
        else:
            messages.error(request, 'El usuario y/o contraseña son incorrectos.')
            return redirect('accounts:signin')