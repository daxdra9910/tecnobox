from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Avg, Count, Sum
from django.urls import reverse
from django.views import View

from apps.shop.models import Product, PurchaseOrder, Review, ShoppingCart, ShoppingCartProduct




class Detail(View):
    """
    Página "Detalles del producto".
    """

    def get(self, request, product_id):
        """
        Muestra la página de detalle junto con las reseñas del producto.
        """
        # Obtenemos el producto.
        product = get_object_or_404(Product, pk=product_id)

        # Determinamos si el usuario autenticado ha comprado ese producto alguna vez.
        # Solo los usuarios que han adquirido el producto pueden dejar una reseña.
        user = request.user
        has_bought = False
        if user.is_authenticated:
            has_bought = PurchaseOrder.objects.filter(user=user, status='D', shopping_cart__shoppingcartproduct__product=product).exists()

        # Obtenemos las fotografías del producto.
        photos = product.photos.all()

        # Obtenemos las reseñas del producto y otros datos relacionados.
        # En realidad solo se obtienen las 100 reseñas más recientes.
        reviews = product.reviews.all().order_by('created_at').reverse()[:100]

        # Número de reseñas que se mostrarán inicialmente.
        reviews_displayed = 3

        # Promedio de puntaje de todas las reseñas del producto.
        average_rating = Review.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg']
        average_rating = round(average_rating, 1) if average_rating else None

        # Recuento de reseñas por cada puntaje (1, 2, 3, 4, 5).
        counts = Review.objects.filter(product=product).values('rating').annotate(count=Count('rating')).order_by('rating')
        rating_counts = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 }

        for rating_count in counts:
            rating = rating_count['rating']
            count = rating_count['count']
            rating_counts[rating] = count

        # Recuento total de reseñas del producto.
        total_reviews = Review.objects.filter(product=product).count()

        # El usuario solo puede reseñar una vez un producto.
        has_reviewed = False
        if user.is_authenticated:
            has_reviewed = Review.objects.filter(user=user, product=product).exists()

        # Obtenemos los descuentos del producto.
        discounts = product.discounts.all()
        discount_value = discounts.aggregate(total=Sum('discount_value'))['total']
        discount_percentage = discounts.aggregate(total=Sum('discount__percentage'))['total']

        # Obtenemos el precio final del producto.
        if discount_value:
            total = product.price - discount_value
        else:
            total = product.price

        # Definimos el contexto de la plantilla.
        context = {
            'product': product,
            'photos': photos,
            'discount_percentage': discount_percentage,
            'total': total,
            'has_bought': has_bought,
            'reviews': reviews,
            'total_reviews': total_reviews,
            'reviews_displayed': reviews_displayed,
            'average_rating': average_rating,
            'rating_counts': rating_counts,
            'has_reviewed': has_reviewed,
        }

        return render(request, 'shop/detail/detail.html', context)


    def post(self, request, product_id):
        """
        Añade una cantidad del producto al carrito de compras.
        """
        # Obtenemos el usuario autenticado.
        user = request.user

        # Si el usuario no está autenticado, lo redirige a la página de inicio de sesión.
        if not user.is_authenticated:
            messages.warning(request, '¡Debes iniciar sesión primero antes de realizar una compra!')
            return redirect('accounts:signin')

        # Obtenemos los datos del formulario
        quantity = request.POST['quantity']

        # Obtenemos el producto.
        product = Product.objects.get(pk=product_id)

        # Obtenemos el carrito de compras activo del usuario o lo creamos si no existe.
        shopping_cart, _ = ShoppingCart.objects.get_or_create(user=user, is_active=True)

        # Creamos la instancia del producto en el carrito de compras.
        ShoppingCartProduct.objects.create(
            product=product,
            cart=shopping_cart,
            amount=quantity
        )

        # Redirigimos al usuario de nuevo a la vista de detalles.
        messages.success(request, '¡Haz añadido el producto al carrito de compras!')
        return redirect(reverse('shop:detail', args=[product_id]))




class MakeReview(View):
    """
    Guarda en la base de datos las reseñas que escriban los usuarios.
    """

    def post(self, request, product_id):
        # Obtenemos los datos del formulario.
        comment = request.POST['comment']
        rating = request.POST['rating']

        # Obtenemos el usuario autenticado.
        user = request.user

        # Obtenemos el producto.
        product = Product.objects.get(pk=product_id)

        # Creamos la reseña.
        Review.objects.create(
            user=user,
            product=product,
            rating=rating,
            comment=comment
        )

        # Redirigimos al usuario de nuevo a la vista de detalles.
        messages.success(request, '¡Ahora los demás podrán ver tu reseña!')
        return redirect(reverse('shop:detail', args=[product_id]))