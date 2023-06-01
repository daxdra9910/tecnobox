from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.views import View
from django.db.models import Sum
from apps.shop.models import ShoppingCartProduct




class ContactUs(View):
    """
    Página "Contáctenos".
    """

    def get(self, request):
        """
        Muestra el formulario de contacto.
        """
        # User
        user = request.user

        # Carrito de compras
        count_cart_products = ShoppingCartProduct.objects.filter(
            cart__user=user,
            cart__is_active=True
        ).aggregate(total_productos=Sum('amount'))

        context = {
            'user' : user,
            'count_cart_products' : count_cart_products['total_productos'] or 0,
            'path' : request.path
        }
        return render(request, 'shop/contact_us.html', context)


    def post(self, request):
        """
        Envia un mensaje del usuario al correo de la empresa.
        (la dirección de correo está definida en config/.env).
        """
        # Obtenemos los datos del formulario.
        full_name = request.POST['full_name']
        phone = request.POST.get('phone', 'No proporcionado')
        email = request.POST['email']
        message = request.POST['message']

        # Enviamos el email.
        from_email = settings.EMAIL_HOST_USER
        to_list = [settings.EMAIL_HOST_USER]
        subject = 'Mensaje enviado desde el sitio web'
        message = f'Nombre: {full_name}\nEmail: {email}\nTeléfono: {phone}\nMensaje: {message}'

        send_mail(subject, message, from_email, to_list, fail_silently=False)

        # Redirigimos al usuario de nuevo a la vista de contacto.
        messages.success(request, '¡Tu mensaje ha sido enviado!')
        return redirect('shop:contact-us')