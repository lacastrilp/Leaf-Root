from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from .models import Order
from users.models import Customer
from carrito.models import Cart, ItemCart
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from .services import create_sales_invoice
from django.shortcuts import redirect
from .models import OrderItem

class GenerateInvoicePDF(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        # Verificar que la orden pertenece al usuario
        if order.customer.user != request.user:
            return HttpResponse("Unauthorized", status=403)
        pdf_buffer = create_sales_invoice(order.id_order)
        return FileResponse(pdf_buffer, as_attachment=True, filename=f"factura_{order.id_order}.pdf")


@login_required
def checkout_review(request):
    """Muestra la info del cliente y los items del carrito antes de confirmar la compra"""
    customer = get_object_or_404(Customer, user=request.user)
    cart = get_object_or_404(Cart, customer=customer)
    items = ItemCart.objects.filter(cart=cart)

    total = sum([item.get_subtotal() for item in items])

    return render(request, "ordenes/checkout_review.html", {
        "customer": customer,
        "cart": cart,
        "items": items,
        "total": total,
    })


@login_required
def checkout_finalize(request):
    """Finaliza la compra: crea la orden, descuenta stock, limpia carrito y genera factura PDF"""
    customer = get_object_or_404(Customer, user=request.user)
    cart = get_object_or_404(Cart, customer=customer)
    items = ItemCart.objects.filter(cart=cart)

    if not items.exists():
        return redirect("cart_detail")

    # 1️⃣ Crear la orden
    order = Order.objects.create(
        cart=cart,
        customer=customer,
        status="Pagado",  # directamente pagado por simplicidad
        order_date=timezone.now()
    )

    # 2️⃣ Crear OrderItems y restar stock
    for item in items:
        # Crear item histórico
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price  # precio al momento de la compra
        )
        # Restar stock
        if item.product.stock >= item.quantity:
            item.product.stock -= item.quantity
            item.product.save()

    # 3️⃣ Vaciar el carrito
    items.delete()

    # 4️⃣ Generar PDF de la factura usando OrderItem en lugar de ItemCart
    pdf_buffer = create_sales_invoice(order.id_order)

    # 5️⃣ Retornar PDF
    return FileResponse(pdf_buffer, as_attachment=True, filename=f"factura_{order.id_order}.pdf")

@login_required
def my_orders(request):
    """
    Muestra el historial de órdenes del usuario autenticado,
    incluyendo el total de cada orden y sus items.
    """
    customer = get_object_or_404(Customer, user=request.user)

    # Obtener órdenes del usuario, más recientes primero
    orders_queryset = Order.objects.filter(customer=customer).order_by('-order_date')

    # Construir lista con total de cada orden
    orders_with_totals = []
    for order in orders_queryset:
        id = order.id_order
        date = order.order_date
        estados = order.status    
        items = order.items.all() # type: ignore
        total = sum([item.get_subtotal() for item in items])
        orders_with_totals.append({
            "order": order,
            "items": items,
            "total": total,
        })

    return render(request, "ordenes/my_orders.html", {
        "orders": orders_with_totals
    })

