from users.models import Customer
from carrito.models import Cart
from catalogo.models import Wishlist

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