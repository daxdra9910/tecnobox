from django.urls import path

from apps.shop import views




app_name = 'shop'


urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('about-us/', views.AboutUs.as_view(), name='about-us'),
    path('contact-us/', views.ContactUs.as_view(), name='contact-us'),
    path('products/', views.Products.as_view(), name='products'),
    path('products/<int:product_id>/', views.Detail.as_view(), name='detail'),
    path('products/<int:product_id>/make-review/', views.MakeReview.as_view(), name='make-review'),
    path('discounts/',views.Discounts.as_view(), name='discounts' ),
    path('cart/', views.Cart.as_view(), name='cart'),
    path('increase-quantity/<int:product_id>/', views.Cart.increase_quantity, name='increase-quantity'),
    path('decrease-quantity/<int:product_id>/', views.Cart.decrease_quantity, name='decrease-quantity'),
    path('remove-from-cart/<int:product_id>/', views.Cart.remove_from_cart, name='remove-from-cart'),
    path('empty-car/', views.Cart.empty_cart, name='empty-cart'),
    path('purchase', views.Cart.purchase, name='purchase'),
    path('terms-and-conditions/', views.TermsAndConditions.as_view(), name='terms-and-conditions'),
]