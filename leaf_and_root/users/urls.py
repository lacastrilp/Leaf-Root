from django.urls import path    
from . import views

urlpatterns = [
    # Autenticación
    path("users/login/", views.LoginView.as_view(), name="login"),
    path("users/logout/", views.LogoutView.as_view(), name="logout"),
    path("users/register/", views.RegisterView.as_view(), name="register"),
    path("account/", views.account_home, name="account_home"),
    path("account/info/", views.account_info_view, name="account_info_view"),
    path("account/info/edit/", views.account_info_edit, name="account_info_edit"),
]
