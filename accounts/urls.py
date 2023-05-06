from django.urls import path

from . import views




app_name = 'accounts'


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('signin/', views.SignIn.as_view(), name='signin'),
    path('signout/', views.SignOut.as_view(), name='signout'),

    path('change-password/', views.ChangePassword.as_view(), name='change-password'),
    path('reset-password/', views.AskResetPassword.as_view(), name='ask-reset-password'),
    path('reset/<str:token>/', views.ResetPassword.as_view(), name='reset-password'),
]