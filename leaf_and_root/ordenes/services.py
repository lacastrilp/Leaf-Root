from django.shortcuts import get_object_or_404
from carrito.models import ItemCart
from ordenes.models import Order, OrderItem
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter



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
# ==========================
# Facturación
# ==========================
def create_sales_invoice(order_id):
    """
    Genera una factura en PDF para una orden específica usando OrderItem.
    """
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    order = get_object_or_404(Order, id_order=order_id)

    # ==========================
    # Encabezado
    # ==========================
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(100, height - 50, "Factura de Venta - LEAF & ROOT")

    pdf.setFont("Helvetica", 10)
    pdf.drawString(100, height - 70, f"Orden: {order.id_order}")
    pdf.drawString(100, height - 85, f"Fecha: {order.order_date.strftime('%d/%m/%Y')}")

    # ==========================
    # Datos del Cliente
    # ==========================
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(100, height - 120, "Datos del Cliente:")

    pdf.setFont("Helvetica", 10)
    pdf.drawString(120, height - 135, f"Nombre: {order.customer.name}")
    pdf.drawString(120, height - 150, f"Email: {order.customer.email}")
    pdf.drawString(120, height - 165, f"Dirección: {order.customer.address}")
    pdf.drawString(120, height - 180, f"Teléfono: {order.customer.phone}")

    # ==========================
    # Detalle de Productos
    # ==========================
    y_position = height - 220
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(100, y_position, "Productos:")

    y_position -= 20
    pdf.setFont("Helvetica", 10)

    total = 0
    items = order.items.all()  # type: ignore
    if not items.exists():
        raise ValueError(f"La orden {order.id_order} no tiene OrderItems asociados.")

    for item in items:
        subtotal = item.get_subtotal()
        pdf.drawString(120, y_position, f"- {item.product.name} x {item.quantity}  →  ${subtotal:.2f}")
        total += subtotal
        y_position -= 15

        # Evitar que el texto se salga de la página
        if y_position < 100:
            pdf.showPage()
            y_position = height - 50
            pdf.setFont("Helvetica", 10)

    # ==========================
    # Total
    # ==========================
    y_position -= 20
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(100, y_position, f"TOTAL A PAGAR: ${total:.2f}")

    # Guardar PDF
    pdf.save()
    buffer.seek(0)
    return buffer

