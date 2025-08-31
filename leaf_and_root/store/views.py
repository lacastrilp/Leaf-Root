from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView, FormView
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.contrib.auth import login
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Product, Review, Order
from .forms import RegisterForm, ReviewForm


# -----------------------------
# Home
# -----------------------------
class HomeView(TemplateView):
    template_name = "storage/home.html"


# -----------------------------
# Productos
# -----------------------------
class ProductDetailView(DetailView):
    model = Product
    template_name = "storage/product_detail.html"
    pk_url_kwarg = "product_id"


class ProductSearchView(ListView):
    model = Product
    template_name = "storage/product_search.html"
    context_object_name = "products"

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        return Product.objects.filter(name__icontains=query)


# -----------------------------
# Autenticación
# -----------------------------
class LoginView(AuthLoginView):
    template_name = "storage/login.html"


class LogoutView(AuthLogoutView):
    next_page = "/"


class RegisterView(FormView):
    template_name = "storage/register.html"
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("home")


# -----------------------------
# Carrito (ejemplo simple)
# -----------------------------
class AddToCartView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        # TODO: Implementar carrito con sesión o modelo Cart
        return HttpResponse(f"{product.name} agregado al carrito")


class RemoveFromCartView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        # TODO: Implementar lógica real de eliminación del carrito
        return HttpResponse(f"{product.name} eliminado del carrito")


# -----------------------------
# Reseñas
# -----------------------------
class SubmitReviewView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
        return redirect("product_detail", product_id=product.id)


class ModerateReviewView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff  # Solo admins pueden moderar

    def get(self, request, review_id):
        review = get_object_or_404(Review, pk=review_id)
        review.approved = True
        review.save()
        return HttpResponse("Reseña moderada")


# -----------------------------
# Administración
# -----------------------------
class AdminDashboardView(UserPassesTestMixin, TemplateView):
    template_name = "storage/admin_dashboard.html"

    def test_func(self):
        return self.request.user.is_staff  # Solo staff puede entrar

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.all()
        context["orders"] = Order.objects.all()
        context["reviews"] = Review.objects.filter(approved=False)
        return context


# -----------------------------
# Facturación
# -----------------------------
class GenerateInvoicePDF(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        # TODO: Generar PDF real con reportlab/weasyprint
        return HttpResponse(f"Factura PDF generada para la orden {order.id}")
