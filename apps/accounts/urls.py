from django.urls import path

from apps.accounts import views




app_name = 'accounts'


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('signin/', views.SignIn.as_view(), name='signin'),
    path('signout/', views.SignOut.as_view(), name='signout'),

    path('profile/', views.Profile.as_view(), name='profile'),
    path('profile/update', views.UpdateProfile.as_view(), name='update-profile'),
    path('profile/change-photo', views.ChangeProfilePhoto.as_view(), name='change-photo'),
    path('profile/delete-photo', views.DeleteProfilePhoto.as_view(), name='delete-photo'),
    path('profile/delete-address', views.DeleteProfileAddress.as_view(), name='delete-address'),
    path('profile/add-address', views.AddProfileAddress.as_view(), name='add-address'),
    path('profile/delete', views.DeleteAccount.as_view(), name='delete-account'),

    path('change-password/', views.ChangePassword.as_view(), name='change-password'),
    path('reset-password/', views.AskResetPassword.as_view(), name='ask-reset-password'),
    path('reset/<str:token>/', views.ResetPassword.as_view(), name='reset-password'),
]