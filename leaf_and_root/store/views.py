from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView, FormView
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.contrib.auth import login
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from leaf_and_root.carrito.models import Cart, ItemCart
from leaf_and_root.ordenes.models import Order
from leaf_and_root.catalogo.models import Product, Review, Wishlist
from leaf_and_root.users.models import Customer # 👈 agrega Customer
from .forms import RegisterForm, ReviewForm, ProductForm


# ---------- Solo admins ----------
def is_admin(user):
    return user.is_authenticated and user.is_staff



@user_passes_test(is_admin)
def admin_dashboard(request):
    products = Product.objects.all()
    return render(request, "admin/dashboard.html", {"products": products})




# ---------- Autenticación ----------
class LoginView(AuthLoginView):
    template_name = "auth/login.html"


class LogoutView(AuthLogoutView):
    next_page = "/"


class RegisterView(FormView):
    template_name = "auth/register.html"
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("home")


# ---------- Carrito (simple) ----------
class AddToCartView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        return HttpResponse(f"{product.name} agregado al carrito")


class RemoveFromCartView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        return HttpResponse(f"{product.name} eliminado del carrito")




# ---------- Administración ----------
class AdminDashboardView(UserPassesTestMixin, TemplateView):
    template_name = "admin/dashboard.html"

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.all()
        context["orders"] = Order.objects.all()
        context["reviews"] = Review.objects.filter(approved=False)
        return context


# ---------- Facturación ----------
class GenerateInvoicePDF(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        return HttpResponse(f"Factura PDF generada para la orden {order.pk}")



