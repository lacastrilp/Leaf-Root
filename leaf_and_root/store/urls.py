from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.redirect_to_home , name="home"),
    path("products/admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    # Administración
    path("admin/dashboard/", views.AdminDashboardView.as_view(), name="admin_dashboard"),
        # Apps
    path('cart/', include('carrito.urls')), 
    path('catalogo/', include('catalogo.urls')),
    path('orders/', include('ordenes.urls')),
    path('users/', include('users.urls')),   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
