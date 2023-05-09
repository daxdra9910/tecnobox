from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils import timezone
from django.views import View

from .models import City, Contact, Region, User




class SignUp(View):
    """
    Registro de usuarios
    """

    def get(self, request):
        """
        Muestra el formulario para crear una nueva cuenta de usuario.
        """
        context = {
            'cities': City.cities.all(),
            'regions': Region.regions.all(),
        }
        return render(request, 'accounts/signup/signup.html', context)


    def post(self, request):
        """
        Crea una nueva instancia de Usuario.
        """
        # Obtenemos los datos del formulario.
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password1']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        address = request.POST['address']
        birthdate = request.POST['birthdate']
        city_id = request.POST['city']
        region_id = request.POST['region']
        phone = request.POST['phone']

        # Validamos los datos enviados en el formulario.
        if User.users.filter(email=email):
            messages.error(request, 'El correo electrónico ya está registrado!')
            return redirect('accounts:signup')

        if User.users.filter(username=username):
            messages.error(request, 'El nombre de usuario ya existe! Prueba de nuevo.')
            return redirect('accounts:signup')

        # Creamos el nuevo usuario en la base de datos.
        user = User.users.create_user(username, email, password1)
        user.first_name = first_name
        user.last_name = last_name
        user.birthdate = birthdate
        user.is_active = True
        user.save()

        # Creamos el registro correspondiente en la tabla de Contacto.
        city = City.cities.get(pk=city_id)
        region = Region.regions.get(pk=region_id)

        contact = Contact(
            user=user,
            region=region,
            city=city,
            address=address,
            phone=phone
        )
        contact.save()

        # Mostramos un mensaje indicando que el proceso ha sido exitoso.
        messages.success(
            request,
            'Tu cuenta ha sido creada correctamente. '
            'Ahora puede iniciar sesión.')

        # Redirigimos al usuario a la vista de login para que inicie sesión.
        return redirect('accounts:signin')




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
                response = redirect('app:home')
                response.set_cookie('remember_me', user.pk, max_age=30)
                return response

            return redirect('app:home')

        # Si el usuario no existe, mostramos el formulario con un mensaje de error.
        else:
            messages.error(request, 'El usuario y/o contraseña son incorrectos.')
            return redirect('accounts:signin')




class SignOut(View):
    """
    Cierre de sesión de usuario actual.
    """

    def get(self, request):
        logout(request)
        messages.success(request, '¡Cierre de sesión exitoso!')
        return redirect('app:home')




class ChangePassword(View):
    """
    Cambia la contraseña del usuario autenticado.
    """

    def get(self, request):
        """
        Muestra el formulario para cambiar la contraseña.
        """
        if not request.user.is_authenticated:
            return redirect('accounts:signin')
        return render(request, 'accounts/change_password.html')


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




class AskResetPassword(View):
    """
    Muestra un formulario para que el usuario ingrese el correo electrónico a
    donde recibirá un enlace para restablecer la contraseña.
    """

    def get(self, request):
        """
        Muestra el formulario para recibir un correo de restablecimiento de contraseña.
        """
        return render(request, 'accounts/reset_password/reset.html')


    def post(self, request):
        """
        Envía un correo electrónico con un enlace para restablecer la contraseña.
        """
        # Obtenemos el email del formulario.
        email = request.POST['email']

        try:
            # Buscamos el usuario en la base de datos.
            user = User.users.get(email=email)
        except User.DoesNotExist:
            # Si el usuario no existe recargamos la página y mostramos un mensaje de advertencia.
            messages.error(request, 'El correo electrónico no está registrado en nuestro sistema.')
            return redirect('accounts:reset-password')

        # Generamos un token único para el usuario.
        token = user.generate_password_reset_token()

        # Enviamos un correo electrónico con el enlace.
        current_site = get_current_site(request)

        from_email = f'TecnoBox <{settings.EMAIL_HOST_USER}>'
        to_list = [user.email]

        subject = 'Instrucciones para restablecer tu contraseña'
        message = render_to_string('accounts/reset_password/email.html', {
            'full_name': user.get_full_name(),
            'domain': current_site.domain,
            'token': token,
        })

        send_mail(subject, message, from_email, to_list, fail_silently=False)

        return render(request, 'accounts/reset_password/reset_done.html')




class ResetPassword(View):
    """
    Muestra un formulario donde el usuario puede restablecer su contraseña.
    """

    def get(self, request, token):
        """
        Muestra el formulario para restablecer la contraseña.
        """
        try:
            # Buscamos el usuario que tenga el token.
            user = User.users.get(password_reset_token=token)

        except User.DoesNotExist:
            # Si el token no es válido, redirigimos a la página de inicio.
            return redirect('app:home')

        # Si el token ha expirado, redirigimos a la página de inicio.
        if user.password_reset_token_created_at < (timezone.now() - timezone.timedelta(hours=1)):
            return redirect('app:home')

        return render(request, 'accounts/reset_password/reset_confirm.html', {'token': token})


    def post(self, request, token):
        # Obtenemos los datos del formulario.
        password = request.POST['password1']

        # Obtenemos el usuario autenticado.
        user = User.users.get(password_reset_token=token)

        # Actualizamos la contraseña y removemos el token.
        user.set_password(password)
        user.password_reset_token = None
        user.password_reset_token_created_at = None
        user.save()

        # Redirigimos al usuario a una página que indica que el proceso ha sido exitoso.
        return render(request, 'accounts/reset_password/reset_complete.html')




class CitiesByRegion(View):
    """
    Muestra un objeto JSON con las ciudades de un departamento dado.
    Esto con el fin de servir datos que sean consumibles por JavaScript.
    """

    def get(self, request, region_id):
        region = Region.regions.get(pk=region_id)
        cities = City.cities.filter(region=region_id)
        data = []

        for city in cities:
            item = {
                'id': city.id,
                'name': city.name,
            }
            data.append(item)

        # Como los datos no son un diccionario, se usa safe=False.
        return JsonResponse(data, safe=False)