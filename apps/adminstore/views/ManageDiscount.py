from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views import View

from apps.shop.models import Discount




class ManageDiscount(UserPassesTestMixin, View):
    """
    Gestiona los descuentos disponibles en la tienda virtual.
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
        return super(ManageDiscount, self).dispatch(*args, **kwargs)


    def get(self, request):
        """
        Muestra la tabla con los descuentos existentes en la base de datos.
        """
        # Obtenemos todas los descuentos.
        discounts = Discount.objects.filter(is_active=True).order_by('pk')

        # Obtenemos el valor del cuadro de búsqueda.
        query = request.GET.get('q')

        # Si se ingresó algo en el cuadro de búsqueda, se filtran los descuentos.
        if query:
            discounts = discounts.filter(
                Q(name__icontains=query) |
                Q(percentage__icontains=query)
            )

        # Creamos el objeto paginador.
        obj_per_page = 25
        paginator = Paginator(discounts, obj_per_page)
        num_page = request.GET.get('page')

        try:
            page = paginator.get_page(num_page)
        except EmptyPage:
            # Si la URL no tiene ?page= devuelve la primera página.
            page = paginator.get_page(1)

        context = {
            'discounts': discounts,
            'page': page,
        }

        return render(request, 'adminstore/discount/show.html', context)


    def post(self, request):
        """
        Agrega un nuevo descuento a la base de datos.
        """
        # Obtenemos los datos del formulario.
        name = request.POST.get('name')
        percentage = request.POST.get('percentage')
        created_at = request.POST.get('created_at')
        finish_at = request.POST.get('finish_at')

        # Creamos el registro en la base de datos.
        Discount.objects.create(
            name=name,
            percentage=percentage,
            created_at=created_at,
            finish_at=finish_at
        )

        # Redirigimos a la misma página de gestión de descuentos.
        messages.success(request, '¡Haz agregado un nuevo descuento!')
        return redirect('adminstore:discounts')


    def put(self, request):
        """
        Actualiza un descuento en la base de datos.
        """
        # Obtenemos los datos del formulario.
        discount_id = request.POST['id']
        name = request.POST['name']
        percentage = request.POST['percentage']
        created_at = request.POST['created_at']
        finish_at = request.POST['finish_at']

        # Obtenemos el descuento de la base de datos.
        discount = Discount.objects.get(pk=discount_id)

        # Actualizamos el registro.
        discount.name = name
        discount.percentage = percentage
        discount.created_at = created_at
        discount.finish_at = finish_at
        discount.save()

        # Redirigimos a la misma página de gestión de descuentos.
        messages.success(request, '¡Haz modificado un descuento!')
        return redirect('adminstore:discounts')


    def delete(self, request):
        """
        Elimina un descuento de la base de datos.
        """
        # Obtenemos los datos del formulario.
        discount_id = request.POST['id']

        # Obtenemos el descuento de la base de datos.
        discount = Discount.objects.get(pk=discount_id)

        # Actualizamos el registro.
        discount.is_active = False
        discount.save()

        # Redirigimos a la misma página de gestión de descuentos.
        messages.warning(request, '¡Haz eliminado un descuento!')
        return redirect('adminstore:discounts')