from django.shortcuts import get_object_or_404
from carrito.models import Cart, ItemCart
from catalogo.models import Product


# ==========================
# Carrito
# ==========================
def add_product_to_cart(cart_id, product_id, quantity=1):
    """Agrega un producto al carrito o actualiza su cantidad."""
    cart = get_object_or_404(Cart, id_cart=cart_id)
    product = get_object_or_404(Product, id_product=product_id)
    item_cart, created = ItemCart.objects.get_or_create(cart=cart, product=product)
    if not created:
        item_cart.quantity += quantity
    else:
        item_cart.quantity = quantity
    item_cart.save()
    return item_cart


def remove_product_from_cart(cart_id, product_id):
    """Elimina un producto del carrito."""
    cart = get_object_or_404(Cart, id_cart=cart_id)
    product = get_object_or_404(Product, id_product=product_id)
    item_cart = get_object_or_404(ItemCart, cart=cart, product=product)
    item_cart.delete()


def clear_cart(cart_id):
    """Vacía todos los items del carrito."""
    cart = get_object_or_404(Cart, id_cart=cart_id)
    ItemCart.objects.filter(cart=cart).delete()


def calculate_cart_total(cart_id):
    """Calcula el costo total del carrito."""
    cart = get_object_or_404(Cart, id_cart=cart_id)
    return sum(item.get_subtotal() for item in ItemCart.objects.filter(cart=cart))
