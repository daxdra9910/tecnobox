from io import BytesIO
import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.views import View
from apps.shop.models import ShoppingCart, ShoppingCartProduct

from PIL import Image

from apps.accounts.models import City, Contact, Region




class Profile(LoginRequiredMixin, View):
    """
    Muestra la página con la información de perfil del usuario autenticado.
    """
    login_url = reverse_lazy('accounts:signin')

    def get(self, request):
        """
        Muestra la información de perfil del usuario autenticado.
        """
        user = request.user
        contacts = Contact.objects.filter(user=user.id, is_active=True)

        if user.is_authenticated:
            # Obtener el carrito del usuario
            try:
                shopping_cart = ShoppingCart.objects.get(user=user, is_active=True)
            except ShoppingCart.DoesNotExist:
                shopping_cart = None
            
            # Obtener la cantidad de productos en el carrito
            if shopping_cart:
                product_count = ShoppingCartProduct.objects.filter(cart=shopping_cart).count()
            else:
                product_count = 0
        else:
            product_count = None

        context = {
            'user': user,
            'contacts': contacts,
            'products_cart_count': product_count
        }

        return render(request, 'accounts/profile/profile.html', context)




class ChangeProfilePhoto(LoginRequiredMixin, View):
    """
    Cambia la foto de perfil del usuario autenticado.
    """
    login_url = reverse_lazy('accounts:signin')

    def post(self, request):
        """
        Valida que el archivo enviado sea una imagen y actualiza
        la foto de perfil del usuario autenticado en la base de datos.
        """
        # Obtenemos el archivo subido.
        uploaded_file = request.FILES.get('photo')

        # Verificamos que el archivo sea una imagen.
        try:
            img = Image.open(uploaded_file)
        except Exception:
            messages.error(request, '¡El archivo no es una imagen!')
            return redirect('accounts:profile')

        # Obtenemos el usuario autenticado.
        user = request.user

        # Redimensionamos la imagen.
        width, height = img.size
        shortest_side = min(width, height)
        new_img = Image.new('RGB', (shortest_side, shortest_side), (255, 255, 255))
        new_img.paste(img, ((shortest_side - width) // 2, (shortest_side - height) // 2))
        new_img = new_img.resize((200, 200))
        buf = BytesIO()
        new_img.save(buf, format='JPEG')
        new_file = InMemoryUploadedFile(buf, None, 'filename.jpg', 'image/jpeg', buf.tell(), None)

        # Eliminamos la foto de perfil si ya existe una anterior.
        if user.photo:
            storage = user.photo.storage
            storage.delete(user.photo.path)

        # Actualizamos la foto del usuario.
        user.photo.save(f'photo_{user.pk}.jpg', new_file, save=False)
        user.save()

        # Redirigimos a la página del perfil de usuario.
        messages.success(request, '¡La foto de perfil ha sido actualizada!')
        return redirect('accounts:profile')




class DeleteProfilePhoto(LoginRequiredMixin, View):
    """
    Elimina la foto de perfil del usuario autenticado.
    """
    login_url = reverse_lazy('accounts:signin')

    def post(self, request):
        """
        Reemplaza la foto de perfil por una imagen genérica.
        """
        # Obtenemos el usuario autenticado.
        user = request.user

        # Eliminamos la foto de perfil si ya existe una anterior.
        if user.photo:
            storage = user.photo.storage
            storage.delete(user.photo.path)

            user.photo = ''
            user.save()

        # Redirigimos a la página del perfil de usuario.
        messages.success(request, '¡La foto de perfil ha sido eliminada!')
        return redirect('accounts:profile')




class DeleteProfileAddress(LoginRequiredMixin, View):
    """
    Elimina una dirección asociada con el perfil del usuario autenticado.
    """
    login_url = reverse_lazy('accounts:signin')

    def post(self, request):
        """
        Elimina la dirección asociada.
        """
        # Obtenemos los datos del formulario.
        contact_id = request.POST['contact_id']

        # Obtenemos la información de contacto.
        contact = Contact.objects.get(pk=contact_id)

        # Eliminamos (ocultamos) la información de contacto.
        contact.is_active = False
        contact.save()

        # Redirigimos a la página del perfil de usuario.
        messages.success(request, '¡La información de contacto ha sido actualizada!')
        return redirect('accounts:profile')




class AddProfileAddress(LoginRequiredMixin, View):
    """
    Agrega una dirección de contacto al perfil del usuario autenticado.
    """
    login_url = reverse_lazy('accounts:signin')

    def get(self, request):
        """
        Muestra el formulario para agregar una nueva dirección de contacto.
        """
        user = request.user

        if user.is_authenticated:
            # Obtener el carrito del usuario
            try:
                shopping_cart = ShoppingCart.objects.get(user=user, is_active=True)
            except ShoppingCart.DoesNotExist:
                shopping_cart = None
            
            # Obtener la cantidad de productos en el carrito
            if shopping_cart:
                product_count = ShoppingCartProduct.objects.filter(cart=shopping_cart).count()
            else:
                product_count = 0
        else:
            product_count = None

        context = {
            'cities': City.objects.filter(is_active=True),
            'regions': Region.objects.filter(is_active=True),
            'products_cart_count': product_count
        }
        return render(request, 'accounts/profile/add_address.html', context)


    def post(self, request):
        """
        Guarda la nueva dirección de contacto en la base de datos.
        """
        # Obtenemos los datos del formulario.
        address = request.POST['address']
        city_id = request.POST['city']
        region_id = request.POST['region']
        phone = request.POST['phone']

        # Obtenemos el usuario autenticado.
        user = request.user

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

        # Redirigimos a la página del perfil de usuario.
        messages.success(request, '¡La información de contacto ha sido actualizada!')
        return redirect('accounts:profile')




class UpdateProfile(LoginRequiredMixin, View):
    """
    Actualiza la información del usuario autenticado.
    """
    login_url = reverse_lazy('accounts:signin')

    def get(self, request):
        """
        Muestra el formulario para actualizar la información personal del usuario.
        """
        user = request.user

        if user.is_authenticated:
            # Obtener el carrito del usuario
            try:
                shopping_cart = ShoppingCart.objects.get(user=user, is_active=True)
            except ShoppingCart.DoesNotExist:
                shopping_cart = None
            
            # Obtener la cantidad de productos en el carrito
            if shopping_cart:
                product_count = ShoppingCartProduct.objects.filter(cart=shopping_cart).count()
            else:
                product_count = 0
        else:
            product_count = None

        context = {
            'user': user,
            'products_cart_count': product_count
        }
        return render(request, 'accounts/profile/update_user.html', context)


    def post(self, request):
        """
        Guarda la información del usuario en la base de datos.
        """
        # Obtenemos los datos del formulario.
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        birthdate = request.POST['birthdate']

        # Obtenemos el usuario autenticado.
        user = request.user

        # Actualizamos la información del usuario.
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        user.birthdate = birthdate
        user.save()

        # Redirigimos a la página del perfil de usuario.
        messages.success(request, '¡La información personal ha sido actualizada!')
        return redirect('accounts:profile')




class DeleteAccount(LoginRequiredMixin, View):
    """
    Elimina la cuenta de usuario.
    """
    login_url = reverse_lazy('accounts:signin')

    def get(self, request):
        """
        Muestra el formulario para eliminar la cuenta de usuario.
        """
        user = request.user

        if user.is_authenticated:
            # Obtener el carrito del usuario
            try:
                shopping_cart = ShoppingCart.objects.get(user=user, is_active=True)
            except ShoppingCart.DoesNotExist:
                shopping_cart = None
            
            # Obtener la cantidad de productos en el carrito
            if shopping_cart:
                product_count = ShoppingCartProduct.objects.filter(cart=shopping_cart).count()
            else:
                product_count = 0
        else:
            product_count = None

        context = {
            'user': user,
            'products_cart_count': product_count
        }
        return render(request, 'accounts/profile/delete_account.html', context)


    def post(self, request):
        """
        Actualiza la información del usuario en la base de datos.
        El usuario en realidad no se elimina, solo se deshabilita.
        """
        # Obtenemos el usuario autenticado.
        user = request.user

        # Desactivamos la cuenta de usuario.
        user.is_active = False
        user.save()

        # Eliminamos la foto de perfil si ya existe una anterior.
        if user.photo:
            storage = user.photo.storage
            storage.delete(user.photo.path)

            user.photo = ''
            user.save()

        # Redirigimos a la página del inicio de sesión.
        messages.success(request, '¡Tu cuenta de usuario ha sido eliminada!')
        return redirect('accounts:signin')