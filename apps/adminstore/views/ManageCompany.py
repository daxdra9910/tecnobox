from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect, render
from django.views import View

from apps.shop.models import Company




class ManageCompany(UserPassesTestMixin, View):
    """
    Gestiona la información de la tienda virtual.
    """
    http_method_names = ['get', 'post', 'put']


    def test_func(self):
        """
        Solamente están autorizados a acceder a esta página los
        usuarios con el atributo is_staff=True.
        """
        return self.request.user.is_staff


    def handle_no_permission(self):
        """
        Si un usuario tiene acceso denegado, se redirecciona al inicio.
        """
        messages.warning(self.request, '¡Acceso denegado!')
        return redirect('shop:home')


    def dispatch(self, *args, **kwargs):
        """
        Maneja las solicitudes PUT y DELETE a través de un campo
        <input type="hidden" name="_method" value="put|delete">
        debido a que los formulario HTML solo permiten GET o POST.
        """
        method = self.request.POST.get('_method', '').lower()
        if method == 'put':
            return self.put(*args, **kwargs)
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(ManageCompany, self).dispatch(*args, **kwargs)


    def get(self, request):
        """
        Muestra la información de la tienda en la base de datos.
        """
        # Obtenemos la información de la tienda.
        company = Company.objects.filter(is_active=True).first()

        context = {
            'company': company,
        }

        return render(request, 'adminstore/company/show.html', context)


    def post(self, request):
        """
        Agrega la información de la tienda en la base de datos.
        """
        # Obtenemos los datos del formulario.
        rut = request.POST['rut']
        name = request.POST['name']
        address = request.POST['address']
        phone = request.POST['phone']
        email = request.POST['email']
        schedule = request.POST['schedule']

        # Creamos el registro de la base de datos.
        Company.objects.create(
            rut=rut,
            name=name,
            address=address,
            phone=phone,
            email=email,
            schedule=schedule
        )

        # Redirigimos a la misma página de gestión de marcas.
        messages.success(request, '¡Haz agregado la información de la tienda!')
        return redirect('adminstore:company')


    def put(self, request):
        """
        Actualiza la información de la tienda en la base de datos.
        """
        # Obtenemos los datos del formulario.
        company_id = request.POST['id']
        rut = request.POST['rut']
        name = request.POST['name']
        address = request.POST['address']
        phone = request.POST['phone']
        email = request.POST['email']
        schedule = request.POST['schedule']

        # Obtenemos el registro de la base de datos.
        company = Company.objects.get(pk=company_id)

        # Actualizamos el registro.
        company.rut = rut
        company.name = name
        company.address = address
        company.phone = phone
        company.email = email
        company.schedule = schedule
        company.save()

        # Redirigimos a la misma página de gestión de marcas.
        messages.success(request, '¡Haz modificado la información de la tienda!')
        return redirect('adminstore:company')