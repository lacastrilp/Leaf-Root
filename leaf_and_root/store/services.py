# Autor: [Tu Nombre]

from django.db.models import Sum, F
from .models import Order, ItemCart, Product
from django.shortcuts import get_object_or_404
from reportlab.pdfgen import canvas
from io import BytesIO

from .models import Product, ItemCart, Order

def get_top_selling_products(limit=3):
    """
    Calcula y retorna los productos más vendidos.
    """
    # Agrupa por producto y suma las cantidades de los ItemCart
    top_products = ItemCart.objects.values('product_id').annotate(
        total_quantity=Sum('quantity')
    ).order_by('-total_quantity')[:limit]

    product_ids = [item['product_id'] for item in top_products]
    return Product.objects.filter(id_product__in=product_ids)

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

    # Suponiendo que la relación de Order a ItemCart está definida
    items = ItemCart.objects.filter(cart=order.cart)
    total = 0
    for item in items:
        subtotal = item.quantity * item.product.price
        pdf.drawString(120, y_position, f"{item.product.name} x {item.quantity} - ${subtotal}")
        total += subtotal
        y_position -= 15

    pdf.drawString(100, y_position - 20, f"Total: ${total}")

    pdf.save()
    buffer.seek(0)
    return buffer
    """
    Obtiene los productos más vendidos.
    """
    top_products_ids = ItemCart.objects.values('product').annotate(
        total_quantity=Sum('quantity')
    ).order_by('-total_quantity')[:limit]
    
    product_ids = [item['product'] for item in top_products_ids]
    return Product.objects.filter(id__in=product_ids)