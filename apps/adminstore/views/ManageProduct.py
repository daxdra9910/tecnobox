from io import BytesIO

from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.paginator import Paginator, EmptyPage
from django.db.models import F, Q, Sum
from django.shortcuts import redirect, render
from django.views import View

from PIL import Image

from apps.shop.models import Brand, Category, Discount, Product, ProductDiscount, ProductPhoto




class ManageProduct(UserPassesTestMixin, View):
    """
    Gestiona los productos disponibles en la tienda virtual.
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
        return super(ManageProduct, self).dispatch(*args, **kwargs)


    def get(self, request):
        """
        Muestra la tabla con los productos existentes en la base de datos.
        """
        # Obtenemos todos los productos con su información relacionada.
        products = Product.objects.select_related(
                'category', 'brand'
            ).prefetch_related(
                'discounts', 'photos'
            ).annotate(
                total_discount=Sum('discounts__discount__percentage')
            ).annotate(
                total_discount_price=F('price') - Sum('discounts__discount_value')
            ).filter(is_active=True).order_by('pk')

        # Obtenemos todas las marcas.
        brands = Brand.objects.filter(is_active=True).order_by('name')

        # Obtenemos todas las categorías.
        categories = Category.objects.filter(is_active=True).order_by('name')

        # Obtenemos todos los descuentos.
        discounts = Discount.objects.filter(is_active=True).order_by('name')

        # Obtenemos el valor del cuadro de búsqueda.
        query = request.GET.get('q')

        # Si se ingresó algo en el cuadro de búsqueda, se filtran los productos.
        if query:
            products = products.filter(
                Q(name__icontains=query) |
                Q(brand__name__icontains=query) |
                Q(category__name__icontains=query)
            )

        # Creamos el objeto paginador.
        obj_per_page = 15
        paginator = Paginator(products, obj_per_page)
        num_page = request.GET.get('page')

        try:
            page = paginator.get_page(num_page)
        except EmptyPage:
            # Si la URL no tiene ?page= devuelve la primera página.
            page = paginator.get_page(1)

        context = {
            'products': products,
            'brands': brands,
            'categories': categories,
            'discounts': discounts,
            'page': page,
        }

        return render(request, 'adminstore/product/show.html', context)


    def post(self, request):
        """
        Agrega un nuevo producto a la base de datos.
        """
        # Obtenemos los datos del formulario.
        brand_id = request.POST.get('brand')
        category_id = request.POST.get('category')
        name = request.POST.get('name')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        description = request.POST.get('description')
        discount_ids = request.POST.getlist('discounts[]')
        photos = request.FILES.getlist('photos')

        # Obtenemos las instancias de marca y categoría.
        brand = Brand.objects.get(pk=brand_id)
        category = Category.objects.get(pk=category_id)

        # Guardamos el nuevo producto en la base de datos.
        product = Product.objects.create(
            name=name,
            description=description,
            price=int(price),
            stock=int(stock),
            brand=brand,
            category=category
        )

        # Para cada descuento creamos el registro en la base de datos.
        for discount_id in discount_ids:
            if discount_id.isdigit():
                discount = Discount.objects.get(pk=discount_id)
                ProductDiscount.objects.create(
                    product=product,
                    discount=discount
                )

        # Para cada foto guardamos el registro en la base de datos.
        for photo in photos:
            # Verificamos que el archivo sea una imagen.
            try:
                Image.open(photo)
            except Exception:
                messages.error(request, '¡El archivo no es una imagen!')
                return redirect('adminstore:products')

            # Creamos el registro en la base de datos.
            product_photo = ProductPhoto.objects.create(product=product)
            product_photo.photo.save('photo.jpg', photo)
            product_photo.save()

        # Redirigimos a la misma página de gestión de productos.
        messages.success(request, '¡Haz agregado un nuevo producto!')
        return redirect('adminstore:products')


    def put(self, request):
        """
        Actualiza una marca en la base de datos.
        """
        # Obtenemos los datos del formulario.
        brand_id = request.POST.get('brand')
        category_id = request.POST.get('category')
        product_id = request.POST.get('id')
        name = request.POST.get('name')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        description = request.POST.get('description')
        discount_ids = request.POST.getlist('discounts[]')
        delete_discounts = request.POST.getlist('delete_discounts[]')
        photos = request.FILES.getlist('photos')
        delete_photos = request.POST.getlist('delete_photos[]')

        # Obtenemos las instancias de marca, categoría y producto.
        brand = Brand.objects.get(pk=brand_id)
        category = Category.objects.get(pk=category_id)
        product = Product.objects.get(pk=product_id)

        # Modificamos los datos del producto.
        product.name = name
        product.brand = brand
        product.category = category
        product.price = price
        product.stock = stock
        product.description = description
        product.save()

        # Para los descuento agregados creamos el registro en la base de datos.
        for discount_id in discount_ids:
            if discount_id.isdigit():
                discount = Discount.objects.get(pk=discount_id)
                ProductDiscount.objects.create(
                    product=product,
                    discount=discount
                )

        # Para los descuentos eliminados modificamos el registro en la base de datos.
        for delete_discount_id in delete_discounts:
            discount = ProductDiscount.objects.get(pk=delete_discount_id)
            discount.is_active = False
            discount.save()

        # Para cada nueva foto guardamos el registro en la base de datos.
        for photo in photos:
            # Verificamos que el archivo sea una imagen.
            try:
                Image.open(photo)
            except Exception:
                messages.error(request, '¡El archivo no es una imagen!')
                return redirect('adminstore:products')

            # Creamos el registro en la base de datos.
            product_photo = ProductPhoto.objects.create(product=product)
            product_photo.photo.save('photo.jpg', photo)
            product_photo.save()

        # Para eliminar las fotos señaladas, las removemos directamente de la base de datos.
        for delete_photo_id in delete_photos:
            product_photo = ProductPhoto.objects.get(pk=delete_photo_id)
            storage = product_photo.photo.storage
            storage.delete(product_photo.photo.path)
            product_photo.delete()

        # Redirigimos a la misma página de gestión de productos.
        messages.success(request, f'¡Haz modificado el producto {product.name}!')
        return redirect('adminstore:products')


    def delete(self, request):
        """
        Elimina un producto de la base de datos.
        """
        # Obtenemos los datos del formulario.
        product_id = request.POST['id']

        # Obtenemos el producto de la base de datos.
        product = Product.objects.get(pk=product_id)

        # Actualizamos el registro.
        product.is_active = False
        product.save()

        # Redirigimos a la misma página de gestión de productos.
        messages.warning(request, '¡Haz eliminado un producto!')
        return redirect('adminstore:products')