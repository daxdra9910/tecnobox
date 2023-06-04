from django.urls import path

from apps.adminstore import views




app_name = 'adminstore'


urlpatterns = [
    path('', views.Metrics.as_view(), name='metrics'),
    path('brands/', views.ManageBrand.as_view(), name='brands'),
    path('categories/', views.ManageCategory.as_view(), name='categories'),
    path('company/', views.ManageCompany.as_view(), name='company'),
    path('discounts/', views.ManageDiscount.as_view(), name='discounts'),
    path('orders/', views.ManageOrder.as_view(), name='orders'),
    path('products/', views.ManageProduct.as_view(), name='products'),
    path('users/', views.ManageUser.as_view(), name='users'),
]