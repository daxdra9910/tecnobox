from django.urls import path

from apps.shop import views




app_name = 'shop'


urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('about-us/', views.AboutUs.as_view(), name='about-us'),
    path('contact-us/', views.ContactUs.as_view(), name='contact-us'),
    path('terms-and-conditions/', views.TermsAndConditions.as_view(), name='terms-and-conditions'),
]