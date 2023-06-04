from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views import View

from apps.shop.models import PurchaseOrder




class ManageOrder(UserPassesTestMixin, View):
    """
    Gestiona las órdenes existentes en la tienda virtual.
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
        return super(ManageOrder, self).dispatch(*args, **kwargs)


    def get(self, request):
        """
        Muestra la tabla con las órdenes existentes en la base de datos.
        """
        # Obtenemos todas los descuentos.
        orders = PurchaseOrder.objects.filter(is_active=True).order_by('pk')

        # Obtenemos el valor del cuadro de búsqueda.
        query = request.GET.get('q')

        # Si se ingresó algo en el cuadro de búsqueda, se filtran las órdenes.
        if query:
            orders = orders.filter(
                Q(subtotal__icontains=query) |
                Q(total__icontains=query) |
                Q(status__icontains=query) |
                Q(payment_method__name__icontains=query) |
                Q(user__username__icontains=query) |
                Q(user__email__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
            )

        # Creamos el objeto paginador.
        obj_per_page = 25
        paginator = Paginator(orders, obj_per_page)
        num_page = request.GET.get('page')

        try:
            page = paginator.get_page(num_page)
        except EmptyPage:
            # Si la URL no tiene ?page= devuelve la primera página.
            page = paginator.get_page(1)

        context = {
            'orders': orders,
            'page': page,
        }

        return render(request, 'adminstore/order/show.html', context)


    def put(self, request):
        """
        Actualiza una órden de compra en la base de datos.
        Desde acá solo se puede actualizar el estado de la órden.
        """
        # Obtenemos los datos del formulario.
        order_id = request.POST['id']
        status = request.POST['status']

        # Obtenemos la órden de la base de datos.
        order = PurchaseOrder.objects.get(pk=order_id)

        # Actualizamos el registro.
        order.status = status
        order.save()

        # Redirigimos a la misma página de gestión de órdenes de compra.
        messages.success(request, '¡Haz modificado el estado de una órden!')
        return redirect('adminstore:orders')