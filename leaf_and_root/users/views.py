from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from .models import Customer
from .forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required
from .forms import CustomerForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

class LoginView(AuthLoginView):
    template_name = "users/login.html"
    form_class = LoginForm

class LogoutView(AuthLogoutView):
    template_name = "users/logout.html"

class RegisterView(FormView):
    template_name = "users/register.html"
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("home")
    
@csrf_exempt
def check_user_email(request):
    username = request.GET.get("username")
    email = request.GET.get("email")
    data = {"username_exists": False, "email_exists": False}

    if username:
        data["username_exists"] = User.objects.filter(username=username).exists()
    if email:
        data["email_exists"] = User.objects.filter(email=email).exists()

    return JsonResponse(data)

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


class ChangePasswordView(PasswordChangeView):
    template_name = 'users/change_password.html'
    success_url = reverse_lazy('account_home')


@login_required
def user_control(request):
    """Vista para que admins gestionen usuarios"""
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('account_home')
    
    if request.method == 'POST':
        # Procesar cambios masivos
        user_ids = request.POST.getlist('user_ids')
        
        for user_id in user_ids:
            try:
                user = User.objects.get(pk=user_id)
                
                # No permitir que el usuario se quite sus propios permisos de admin
                if user.id == request.user.id: # type: ignore
                    continue
                
                # Actualizar estados
                user.is_active = request.POST.get(f'is_active_{user_id}') == 'on'
                user.is_staff = request.POST.get(f'is_staff_{user_id}') == 'on'
                user.is_superuser = request.POST.get(f'is_superuser_{user_id}') == 'on'
                user.save()
            except User.DoesNotExist:
                continue
        
        return redirect('user_control')
    
    users = User.objects.all().select_related('customer').order_by('-date_joined')
    return render(request, 'users/user_control.html', {'users': users})


@login_required
def toggle_admin(request, user_id):
    """Toggle admin status de un usuario"""
    if not (request.user.is_staff or request.user.is_superuser):
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)
    
    if request.method == 'POST':
        user = User.objects.get(pk=user_id)
        user.is_staff = not user.is_staff
        user.save()
        
        return JsonResponse({
            'success': True,
            'is_staff': user.is_staff
        })
    
    return JsonResponse({'success': False}, status=400)


@login_required
def delete_user(request, user_id):
    """Eliminar un usuario"""
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('account_home')
    
    if request.method == 'POST':
        try:
            user = User.objects.get(pk=user_id)
            
            # No permitir eliminar al propio usuario
            if user.id == request.user.id: # type: ignore
                return redirect('user_control')
            
            user.delete()
        except User.DoesNotExist:
            pass
    
    return redirect('user_control')
