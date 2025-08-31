# Autor: [Tu Nombre]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('product/<int:product_id>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('search/', views.ProductSearchView.as_view(), name='search'),
    path('login/', views.LoginView.as_view(), name='login'),
    # Rutas de la sección de administración
    path('admin/dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    # Ruta para la funcionalidad de PDF
    path('order/<int:order_id>/invoice/', views.GenerateInvoicePDF.as_view(), name='generate_invoice_pdf'),
]