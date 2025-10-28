from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

def exclude_admin(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_staff or request.user.is_superuser:
            # Opción A: lanzar error
            raise PermissionDenied("El administrador no tiene carrito de compras.")

            # Opción B: redirigir al inicio
            # return redirect("home")

        return view_func(request, *args, **kwargs)
    return wrapper