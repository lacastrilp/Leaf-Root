from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.product_list, name="home"),
    path("products/admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path('products/add/', views.add_product, name='add_product'),
    path('products/<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('products/<int:pk>/delete/', views.delete_product, name='delete_product'),
    # Productos
    path("products/", views.ProductListView.as_view(), name="product_list"),
    path("product/<int:product_id>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("search/", views.ProductSearchView.as_view(), name="search"),
    # Autenticación
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),

    # Carrito
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),


    # Reseñas
    path("product/<int:product_id>/review/", views.SubmitReviewView.as_view(), name="submit_review"),
    path("review/<int:review_id>/moderate/", views.ModerateReviewView.as_view(), name="moderate_review"),

    # Administración
    path("admin/dashboard/", views.AdminDashboardView.as_view(), name="admin_dashboard"),

    # Facturación
    path("order/<int:order_id>/invoice/", views.GenerateInvoicePDF.as_view(), name="generate_invoice_pdf"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)