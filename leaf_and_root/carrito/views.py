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



@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    customer, _ = Customer.objects.get_or_create(user=request.user)

    quantity = int(request.POST.get('quantity', 1))

    cart, _ = Cart.objects.get_or_create(customer=customer)
    item, created_item = ItemCart.objects.get_or_create(cart=cart, product=product)

    if not created_item:
        item.quantity += quantity
    else:
        item.quantity = quantity
    item.save()

    # 👇 Detectar si la petición es AJAX (fetch) o no
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        print(">>> AJAX:", request.headers.get("x-requested-with"))
        items = []
        for i in ItemCart.objects.filter(cart=cart):
            items.append({
                "id": i.product.id_product,
                "name": i.product.name,
                "quantity": i.quantity,
                "price": float(i.product.price),
                "subtotal": float(i.get_subtotal()),
                "image": i.product.image_url if i.product.image_url else "https://via.placeholder.com/50"
            })

        return JsonResponse({
            "success": True,
            "cart_items": items,
            "total_items": sum(i["quantity"] for i in items),
            "total_price": sum(i["subtotal"] for i in items),
        })

    # Si no es AJAX → redirige al carrito como antes
    return redirect("cart_detail")


@login_required
def remove_from_cart(request, product_id):
    customer = request.user.customer
    cart, created = Cart.objects.get_or_create(customer=customer)

    try:
        item = ItemCart.objects.get(cart=cart, product__id_product=product_id)
    except ItemCart.DoesNotExist:
        # Si no existe el item, simplemente redirige al carrito
        return redirect('cart_detail')

    qty = int(request.POST.get('quantity', 1))
    
    if item.quantity > qty:
        item.quantity -= qty
        item.save()
    else:
        item.delete()
    
    return redirect('cart_detail')


@login_required
def cart_detail(request):
    customer = get_object_or_404(Customer, user=request.user)
    cart, created = Cart.objects.get_or_create(customer=customer)
    items = ItemCart.objects.filter(cart=cart)
    total_price = sum(item.get_subtotal() for item in items)
    total_items = sum(item.quantity for item in items)

    return render(request, 'cart_detail.html', {
        'cart': cart,
        'items': items,
        'total_price': total_price,
        'total_items': total_items
    })

class AddToCartView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        return HttpResponse(f"{product.name} agregado al carrito")


class RemoveFromCartView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        return HttpResponse(f"{product.name} eliminado del carrito")


# Create your views here.
