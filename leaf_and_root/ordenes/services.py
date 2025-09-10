from django.shortcuts import get_object_or_404
from carrito.models import ItemCart
from ordenes.models import Order
from io import BytesIO
from reportlab.pdfgen import canvas



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

