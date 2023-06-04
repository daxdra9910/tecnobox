from django.contrib import admin
from django.urls import path

from apps.utils import views




urlpatterns = [
    path('dashboard/', admin.site.urls),
    path('region/<int:region_id>/cities/', views.CitiesByRegion.as_view(), name='cities-by-region'),
]
