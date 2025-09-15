from django.shortcuts import render
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from .models import Customer
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from .forms import CustomerForm

class LoginView(AuthLoginView):
    template_name = "users/login.html"

class LogoutView(AuthLogoutView):
    template_name = "users/logout.html"

class RegisterView(FormView):
    template_name = "users/register.html"
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("home")

@login_required
def account_home(request):
    return render(request, "users/account_home.html")


@login_required
def account_info_view(request):
    try:
        customer = Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        # si no existe, lo creamos vacío con los datos básicos del user
        customer = Customer.objects.create(
            user=request.user,
            email=request.user.email,  # inicializamos con el correo del user
            name=request.user.username,
        )
    return render(request, "users/account_info_view.html", {"customer": customer})


@login_required
def account_info_edit(request):
    """Vista para editar los datos del customer"""
    customer, created = Customer.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect("account_info_view")  # 👉 vuelve a la vista de visualización
    else:
        form = CustomerForm(instance=customer)

    return render(request, "users/account_info_edit.html", {"form": form})
    # buscar el customer del usuario logueado
