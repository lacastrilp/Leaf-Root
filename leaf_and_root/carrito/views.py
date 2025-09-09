from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from leaf_and_root.catalogo.models import Product
from leaf_and_root.users.models import Customer 
from leaf_and_root.carrito.models import Cart, ItemCart

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    customer = get_object_or_404(Customer, user=request.user)

    quantity = int(request.POST.get('quantity', 1))

    cart, created = Cart.objects.get_or_create(customer=customer)
    item, created_item = ItemCart.objects.get_or_create(cart=cart, product=product)

    if not created_item:
        item.quantity += quantity
    else:
        item.quantity = quantity
    item.save()

    return redirect('cart_detail')

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

    return render(request, 'cart/cart_detail.html', {
        'cart': cart,
        'items': items,
        'total_price': total_price,
        'total_items': total_items
    })


# Create your views here.
