# Autor: [Tu Nombre]

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

from .models import Product
from .services import get_top_selling_products, create_sales_invoice


from .forms import CustomerRegistrationForm

class ProductListView(ListView):
    model = Product
    template_name = 'store/home.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_products'] = get_top_selling_products(3)
        return context

class CustomerLoginView(LoginRequiredMixin, ListView):
    # La vista para el panel de usuario final
    template_name = 'store/customer_dashboard.html'
    # ... (lógica de la vista) ...

class AdminDashboardView(LoginRequiredMixin, ListView):
    # La vista para el panel de administrador
    template_name = 'store/admin_dashboard.html'
    # ... (lógica de la vista) ...
    

# Vistas de la sección de usuario final

class HomeView(ListView):
    """Muestra la página de inicio con el listado de productos y el top 3 de más vendidos."""
    model = Product
    template_name = 'store/home.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_selling_products'] = get_top_selling_products(3)
        return context

class ProductDetailView(View):
    """Muestra los detalles de un producto específico."""
    def get(self, request, product_id):
        product = get_object_or_404(Product, id_product=product_id)
        return render(request, 'store/product_detail.html', {'product': product})

class ProductSearchView(ListView):
    """Permite la búsqueda de productos por nombre."""
    model = Product
    template_name = 'store/search_results.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        queryset = Product.objects.filter(name__icontains=query)
        # Funcionalidad extra: Filtrado por tipo de producto (vegano/vegetariano)
        is_vegan = self.request.GET.get('vegan') == 'on'
        is_vegetarian = self.request.GET.get('vegetarian') == 'on'

        if is_vegan:
            queryset = queryset.filter(is_vegan=True)
        elif is_vegetarian:
            queryset = queryset.filter(is_vegetarian=True)

        return queryset

# Vistas de autenticación

class LoginView(View):
    """Maneja el inicio de sesión del cliente o administrador."""
    def get(self, request):
        return render(request, 'store/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff: # Asumiendo que los administradores son staff
                return redirect('admin_dashboard')
            else:
                return redirect('customer_dashboard')
        else:
            return render(request, 'store/login.html', {'error': 'Credenciales inválidas.'})

# Vistas de la sección del administrador

class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Panel de administración para la gestión de productos."""
    model = Product
    template_name = 'store/admin/admin_dashboard.html'
    context_object_name = 'products'

    def test_func(self):
        return self.request.user.is_staff

# Vista para generar facturas PDF

class GenerateInvoicePDF(LoginRequiredMixin, View):
    def get(self, request, order_id):
        try:
            # La lógica de creación del PDF se delega a un servicio
            pdf_file = create_sales_invoice(order_id)
            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="factura_{order_id}.pdf"'
            return response
        except Exception as e:
            return HttpResponse(f"Error generando la factura: {e}", status=500)