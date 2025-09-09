from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from leaf_and_root.ordenes.models import Order
from leaf_and_root.catalogo.models import Product, Review


# ---------- Solo admins ----------
def is_admin(user):
    return user.is_authenticated and user.is_staff



@user_passes_test(is_admin)
def admin_dashboard(request):
    products = Product.objects.all()
    return render(request, "admin/dashboard.html", {"products": products})



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




