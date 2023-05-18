from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View

from apps.accounts.models import City, Contact, Region, User




class SignUp(View):
    """
    Registro de usuarios
    """

    def get(self, request):
        """
        Muestra el formulario para crear una nueva cuenta de usuario.
        """
        context = {
            'cities': City.objects.filter(is_active=True),
            'regions': Region.objects.filter(is_active=True),
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
        if User.objects.filter(email=email):
            messages.error(request, 'El correo electrónico ya está registrado!')
            return redirect('accounts:signup')

        if User.objects.filter(username=username):
            messages.error(request, 'El nombre de usuario ya existe! Prueba de nuevo.')
            return redirect('accounts:signup')

        # Creamos el nuevo usuario en la base de datos.
        user = User.objects.create_user(username, email, password1)
        user.first_name = first_name
        user.last_name = last_name
        user.birthdate = birthdate
        user.is_active = True
        user.save()

        # Creamos el registro correspondiente en la tabla de Contacto.
        city = City.objects.get(pk=city_id)
        region = Region.objects.get(pk=region_id)

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