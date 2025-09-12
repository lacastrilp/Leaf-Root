from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from catalogo.models import Product
from users.models import Customer 
from carrito.models import Cart, ItemCart
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import HttpResponse
from django.http import JsonResponse
from .decorators import exclude_admin


def build_cart_response(cart):
    """Helper: genera JSON con items del carrito."""
    items = []
    for i in ItemCart.objects.filter(cart=cart):
        items.append({
            "id": i.product.id_product,
            "name": i.product.name,
            "quantity": i.quantity,
            "price": float(i.product.price),
            "subtotal": float(i.get_subtotal()),
            "image": i.product.image_url if i.product.image_url else "https://via.placeholder.com/50",
        })
    return {
        "success": True,
        "cart_items": items,
        "total_items": sum(i["quantity"] for i in items),
        "total_price": sum(i["subtotal"] for i in items),
    }

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    customer, _ = Customer.objects.get_or_create(user=request.user)
    cart, _ = Cart.objects.get_or_create(customer=customer)

    quantity = int(request.POST.get("quantity", 1))
    item, created_item = ItemCart.objects.get_or_create(cart=cart, product=product)

    if not created_item:
        item.quantity += quantity
    else:
        item.quantity = quantity
    item.save()

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse(build_cart_response(cart))

    return redirect("cart_detail")

@login_required
def remove_from_cart(request, product_id):
    customer, _ = Customer.objects.get_or_create(user=request.user)
    cart, _ = Cart.objects.get_or_create(customer=customer)

    item = get_object_or_404(ItemCart, cart=cart, product_id=product_id)
    item.delete()

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse(build_cart_response(cart))

    return redirect("cart_detail")

@login_required
@exclude_admin
def cart_detail(request):
    # Aquí ya no necesitas preguntar por admin
    customer, _ = Customer.objects.get_or_create(user=request.user)
    cart, _ = Cart.objects.get_or_create(customer=customer)
    items = ItemCart.objects.filter(cart=cart)
    suma = sum(item.get_subtotal() for item in items)
    total_price = round(suma, 2)
    total_items = sum(item.quantity for item in items)

    return render(request, 'cart_detail.html', {
        'cart': cart,
        'items': items,
        'total_price': total_price,
        'total_items': total_items,
        "quantity_range": list(range(1, 11)),
    })

@login_required
def update_cart_quantity(request, product_id):
    customer, _ = Customer.objects.get_or_create(user=request.user)
    cart, _ = Cart.objects.get_or_create(customer=customer)
    item = get_object_or_404(ItemCart, cart=cart, product_id=product_id)
    quantity = int(request.POST.get("quantity", 1))

    if quantity > 0:
        item.quantity = quantity
        item.save()
    else:
        item.delete()

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse(build_cart_response(cart))

    return redirect("cart_detail")

class AddToCartView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        return HttpResponse(f"{product.name} agregado al carrito")

class RemoveFromCartView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        return HttpResponse(f"{product.name} eliminado del carrito")


