from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Product
from .forms import CustomerRegistrationForm
from .services import (
    get_top_selling_products, create_sales_invoice,
    add_product_to_cart, remove_product_from_cart,
    create_new_customer, add_review, moderate_review
)


class HomeView(ListView):
    model = Product
    template_name = "store/home.html"
    context_object_name = "products"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["top_selling_products"] = get_top_selling_products(3)
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "store/product_detail.html"
    pk_url_kwarg = "product_id"
    context_object_name = "product"


class ProductSearchView(ListView):
    model = Product
    template_name = "store/search_results.html"
    context_object_name = "products"

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        return Product.objects.filter(name__icontains=query)


class LoginView(View):
    def get(self, request):
        return render(request, "store/login.html")

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            if user.is_staff:
                return redirect("admin_dashboard")
            return redirect("customer_dashboard")
        return render(request, "store/login.html", {"error": "Credenciales inválidas."})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect("home")


class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Product
    template_name = "store/admin_dashboard.html"
    context_object_name = "products"

    def test_func(self):
        return self.request.user.is_staff


class RegisterView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, "store/register.html", {"form": form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        return render(request, "store/register.html", {"form": form})


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        cart, _ = getattr(request.user.customer, "cart", None), None
        if not cart:
            from .models import Cart
            cart, _ = Cart.objects.get_or_create(customer=request.user.customer)
        add_product_to_cart(cart.id_cart, product_id, quantity=1)
        return redirect("home")


class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        cart = getattr(request.user.customer, "cart", None)
        if cart:
            remove_product_from_cart(cart.id_cart, product_id)
        return redirect("cart_detail")


class SubmitReviewView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        customer = request.user.customer
        comment = request.POST.get("comment")
        rating = request.POST.get("rating")
        add_review(product_id, customer.id_customer, comment, rating)
        return redirect("product_detail", product_id=product_id)


class ModerateReviewView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    def post(self, request, review_id):
        approved = request.POST.get("approved") == "true"
        moderate_review(review_id, approved)
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


class GenerateInvoicePDF(LoginRequiredMixin, View):
    def get(self, request, order_id):
        try:
            pdf_file = create_sales_invoice(order_id)
            response = HttpResponse(pdf_file, content_type="application/pdf")
            response["Content-Disposition"] = f'attachment; filename="factura_{order_id}.pdf"'
            return response
        except Exception as e:
            return HttpResponse(f"Error generando la factura: {e}", status=500)
