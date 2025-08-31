# Autor: [Tu Nombre]

from django.db.models import Sum
from django.shortcuts import get_object_or_404
from io import BytesIO
from reportlab.pdfgen import canvas
from .models import Product, ItemCart, Order, Cart, Wishlist, Review, Customer

# ==========================
# Lógica de Productos
# ==========================
def get_top_selling_products(limit=3):
    """
    Calcula y retorna los productos más vendidos.
    """
    top_products = (
        ItemCart.objects.values('product')
        .annotate(total_quantity=Sum('quantity'))
        .order_by('-total_quantity')[:limit]
    )
    product_ids = [item['product'] for item in top_products]
    return Product.objects.filter(id_product__in=product_ids)


# ==========================
# Facturación
# ==========================
def create_sales_invoice(order_id):
    """
    Genera una factura en formato PDF para una orden específica.
    """
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)

    order = get_object_or_404(Order, id_order=order_id)

    pdf.drawString(100, 750, "Factura de Venta - LEAF & ROOT")
    pdf.drawString(100, 730, f"Orden: {order.id_order}")
    pdf.drawString(100, 710, f"Fecha: {order.order_date}")

    y_position = 680
    pdf.drawString(100, y_position, "Productos:")
    y_position -= 20

    items = ItemCart.objects.filter(cart=order.cart)
    total = 0
    for item in items:
        subtotal = item.get_subtotal()
        pdf.drawString(
            120, y_position,
            f"{item.product.name} x {item.quantity} - ${subtotal:.2f}"
        )
        total += subtotal
        y_position -= 15

    pdf.drawString(100, y_position - 20, f"Total: ${total:.2f}")

    pdf.save()
    buffer.seek(0)
    return buffer


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


# ==========================
# Ordenes y Pagos
# ==========================
def process_order_payment(order_id):
    """Procesa el pago de una orden y actualiza su estado."""
    order = get_object_or_404(Order, id_order=order_id)
    order.status = 'Pagado'
    order.save()
    return True


def cancel_order(order_id):
    """Cancela una orden y retorna el stock de los productos."""
    order = get_object_or_404(Order, id_order=order_id)
    if order.status == 'Pendiente':
        items = ItemCart.objects.filter(cart=order.cart)
        for item in items:
            item.product.stock += item.quantity
            item.product.save()
        order.status = 'Cancelada'
        order.save()
        return True
    return False


# ==========================
# Reseñas
# ==========================
def add_review(product_id, customer_id, comment, rating):
    """Permite a un cliente enviar una reseña para un producto."""
    product = get_object_or_404(Product, id_product=product_id)
    customer = get_object_or_404(Customer, id_customer=customer_id)
    return Review.objects.create(
        product=product,
        customer=customer,
        comment=comment,
        rating=rating,
        approved=False
    )


def create_new_customer(form_data):
    """Crea un nuevo cliente y su carrito asociado."""
    customer = Customer.objects.create(
        name=form_data['name'],
        email=form_data['email'],
        address=form_data['address'],
        phone=form_data['phone'],
        password=form_data['password'] # En un proyecto real, se debería hashear la contraseña
    )
    Cart.objects.create(customer=customer)
    Wishlist.objects.create(customer=customer)
    return customer


def moderate_review(review_id, approved):
    """Modera una reseña, aprobándola o rechazándola."""
    review = get_object_or_404(Review, id_review=review_id)
    review.approved = approved
    review.save()
    return review


# ==========================
# Wishlist
# ==========================
def add_product_to_wishlist(customer_id, product_id):
    """Agrega un producto a la lista de deseos."""
    customer = get_object_or_404(Customer, id_customer=customer_id)
    product = get_object_or_404(Product, id_product=product_id)
    return Wishlist.objects.create(customer=customer, product=product)


def remove_product_from_wishlist(wishlist_id):
    """Elimina una entrada de la lista de deseos."""
    wishlist = get_object_or_404(Wishlist, id_wishlist=wishlist_id)
    wishlist.delete()
