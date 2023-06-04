from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views import View

from apps.accounts.models import User




class ManageUser(UserPassesTestMixin, View):
    """
    Gestiona los usuarios existentes en la tienda virtual.
    Solo permite asignar o quitar los permisos de administración
    a los usuarios del sitio web.
    """
    http_method_names = ['get', 'put']


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
        return super(ManageUser, self).dispatch(*args, **kwargs)


    def get(self, request):
        """
        Muestra la tabla con los usuarios existentes en la base de datos.
        """
        # Obtenemos todas los descuentos.
        users = User.objects.filter(is_active=True).order_by('pk')

        # Obtenemos el valor del cuadro de búsqueda.
        query = request.GET.get('q')

        # Si se ingresó algo en el cuadro de búsqueda, se filtran las órdenes.
        if query:
            users = users.filter(
                Q(username__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(email__icontains=query)
            )

        # Creamos el objeto paginador.
        obj_per_page = 25
        paginator = Paginator(users, obj_per_page)
        num_page = request.GET.get('page')

        try:
            page = paginator.get_page(num_page)
        except EmptyPage:
            # Si la URL no tiene ?page= devuelve la primera página.
            page = paginator.get_page(1)

        context = {
            'users': users,
            'page': page,
        }

        return render(request, 'adminstore/user/show.html', context)


    def put(self, request):
        """
        Actualiza un usuario de la base de datos.
        Desde acá solo se puede convertir o eliminar de los administradores.
        """
        # Obtenemos los datos del formulario.
        user_id = request.POST['id']
        is_staff = request.POST['is_staff']

        # Obtenemos al usuario de la base de datos.
        user = User.objects.get(pk=user_id)

        # Actualizamos el registro.
        user.is_staff = is_staff
        user.save()

        # Redirigimos a la misma página de gestión de usuarios.
        messages.success(request, '¡Haz modificado los permisos de un usuario!')
        return redirect('adminstore:users')