from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views import View

from apps.shop.models import Brand




class ManageBrand(UserPassesTestMixin, View):
    """
    Gestiona las marcas disponibles en la tienda virtual.
    """
    http_method_names = ['get', 'post', 'put', 'delete']


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
        return super(ManageBrand, self).dispatch(*args, **kwargs)


    def get(self, request):
        """
        Muestra la tabla con las marcas existentes en la base de datos.
        """
        # Obtenemos todas las marcas.
        brands = Brand.objects.filter(is_active=True).order_by('pk')

        # Obtenemos el valor del cuadro de búsqueda.
        query = request.GET.get('q')

        # Si se ingresó algo en el cuadro de búsqueda, se filtran las marcas.
        if query:
            brands = brands.filter(
                Q(name__icontains=query)
            )

        # Creamos el objeto paginador.
        obj_per_page = 25
        paginator = Paginator(brands, obj_per_page)
        num_page = request.GET.get('page')

        try:
            page = paginator.get_page(num_page)
        except EmptyPage:
            # Si la URL no tiene ?page= devuelve la primera página.
            page = paginator.get_page(1)

        context = {
            'brands': brands,
            'page': page,
        }

        return render(request, 'adminstore/brand/show_brands.html', context)


    def post(self, request):
        """
        Agrega una nueva marca a la base de datos.
        """
        # Obtenemos los datos del formulario.
        name = request.POST.get('name')

        # Creamos el registro en la base de datos.
        Brand.objects.create(
            name=name,
        )

        # Redirigimos a la misma página de gestión de marcas.
        messages.success(request, '¡Haz agregado una nueva marca!')
        return redirect('adminstore:brands')


    def put(self, request):
        """
        Actualiza una marca en la base de datos.
        """
        # Obtenemos los datos del formulario.
        brand_id = request.POST['id']
        name = request.POST['name']

        # Obtenemos la marca de la base de datos.
        brand = Brand.objects.get(pk=brand_id)

        # Actualizamos el registro.
        brand.name = name
        brand.save()

        # Redirigimos a la misma página de gestión de marcas.
        messages.success(request, '¡Haz modificado una marca!')
        return redirect('adminstore:brands')


    def delete(self, request):
        """
        Elimina una marca de la base de datos.
        """
        # Obtenemos los datos del formulario.
        brand_id = request.POST['id']

        # Obtenemos la marca de la base de datos.
        brand = Brand.objects.get(pk=brand_id)

        # Actualizamos el registro.
        brand.is_active = False
        brand.save()

        # Redirigimos a la misma página de gestión de marcas.
        messages.warning(request, '¡Haz eliminado una marca!')
        return redirect('adminstore:brands')