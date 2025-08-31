from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),

    # Productos
    path('product/<int:product_id>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('search/', views.ProductSearchView.as_view(), name='search'),

    # Autenticación
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),

    # Carrito
    path('cart/add/<int:product_id>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.RemoveFromCartView.as_view(), name='remove_from_cart'),

    # Reseñas
    path('product/<int:product_id>/review/', views.SubmitReviewView.as_view(), name='submit_review'),
    path('review/<int:review_id>/moderate/', views.ModerateReviewView.as_view(), name='moderate_review'),

    # Administración
    path('admin/dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),

    # Facturación
    path('order/<int:order_id>/invoice/', views.GenerateInvoicePDF.as_view(), name='generate_invoice_pdf'),
]
