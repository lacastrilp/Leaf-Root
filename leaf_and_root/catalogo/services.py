from django.db.models import Sum
from django.shortcuts import get_object_or_404
from .models import Product, Review, Wishlist
from carrito.models import ItemCart
from users.models import Customer

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