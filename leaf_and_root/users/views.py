from django.shortcuts import render
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from .forms import RegisterForm

class LoginView(AuthLoginView):
    template_name = "login.html"

class LogoutView(AuthLogoutView):
    template_name = "logout.html"

class RegisterView(FormView):
    template_name = "register.html"
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("home")

# Create your views here.
