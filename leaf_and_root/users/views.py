from django.shortcuts import render
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from .forms import CustomerForm
from .models import Customer
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required

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
    # buscar el customer del usuario logueado
    customer, created = Customer.objects.get_or_create(user=request.user)
    return render(request, "users/account_info_view.html", {"customer": customer})

@login_required
def account_info_edit(request):
    # buscar el customer del usuario logueado
    customer, created = Customer.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect("account_info_view")  # redirigir a la misma página tras guardar
    else:
        form = CustomerForm(instance=customer)

    return render(request, "users/account_info.html", {"form": form})
