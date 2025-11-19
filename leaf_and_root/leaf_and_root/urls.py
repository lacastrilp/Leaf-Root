from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
import django.contrib.auth.views as auth_views  # 👈 para login
from users.forms import LoginForm

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(
            template_name="users/login.html",
            authentication_form=LoginForm,
        ),
        name="login",
    ),
    path('accounts/', include('django.contrib.auth.urls')),  # 👈 importante
    path('', include('store.urls')),  # tus vistas
    path('cart/', include('carrito.urls')),  # carrito
    path('catalog/', include('catalogo.urls')),  # catálogo
    path('users/', include('users.urls')),  # usuarios
    path('store/', include('store.urls')),  # tienda
    path('orders/', include('ordenes.urls')),  # órdenes
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)