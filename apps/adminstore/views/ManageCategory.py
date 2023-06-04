from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views import View

from apps.shop.models import Category




class ManageCategory(UserPassesTestMixin, View):
    """
    Gestiona las categorías disponibles en la tienda virtual.
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
        return super(ManageCategory, self).dispatch(*args, **kwargs)


    def get(self, request):
        """
        Muestra la tabla con las categorías existentes en la base de datos.
        """
        # Obtenemos todas las categorías.
        categories = Category.objects.filter(is_active=True).order_by('pk')

        # Obtenemos el valor del cuadro de búsqueda.
        query = request.GET.get('q')

        # Si se ingresó algo en el cuadro de búsqueda, se filtran las categorías.
        if query:
            categories = categories.filter(
                Q(name__icontains=query)
            )

        # Creamos el objeto paginador.
        obj_per_page = 25
        paginator = Paginator(categories, obj_per_page)
        num_page = request.GET.get('page')

        try:
            page = paginator.get_page(num_page)
        except EmptyPage:
            # Si la URL no tiene ?page= devuelve la primera página.
            page = paginator.get_page(1)

        context = {
            'categories': categories,
            'page': page,
        }

        return render(request, 'adminstore/category/show.html', context)


    def post(self, request):
        """
        Agrega una nueva categoría a la base de datos.
        """
        # Obtenemos los datos del formulario.
        name = request.POST.get('name')

        # Creamos el registro en la base de datos.
        Category.objects.create(
            name=name,
        )

        # Redirigimos a la misma página de gestión de categorías.
        messages.success(request, '¡Haz agregado una nueva categoría!')
        return redirect('adminstore:categories')


    def put(self, request):
        """
        Actualiza una categoría en la base de datos.
        """
        # Obtenemos los datos del formulario.
        category_id = request.POST['id']
        name = request.POST['name']

        # Obtenemos la categoría de la base de datos.
        category = Category.objects.get(pk=category_id)

        # Actualizamos el registro.
        category.name = name
        category.save()

        # Redirigimos a la misma página de gestión de categoría.
        messages.success(request, '¡Haz modificado una categoría!')
        return redirect('adminstore:categories')


    def delete(self, request):
        """
        Elimina una categoría de la base de datos.
        """
        # Obtenemos los datos del formulario.
        category_id = request.POST['id']

        # Obtenemos la marca de la base de datos.
        category = Category.objects.get(pk=category_id)

        # Actualizamos el registro.
        category.is_active = False
        category.save()

        # Redirigimos a la misma página de gestión de categorías.
        messages.warning(request, '¡Haz eliminado una categoría!')
        return redirect('adminstore:categories')