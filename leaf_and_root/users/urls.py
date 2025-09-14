from django.urls import path    
from . import views

urlpatterns = [
    # Autenticación
    path("users/login/", views.LoginView.as_view(), name="login"),
    path("users/logout/", views.LogoutView.as_view(), name="logout"),
    path("users/register/", views.RegisterView.as_view(), name="register"),

]
