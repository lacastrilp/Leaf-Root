# Autor: [Tu Nombre]

from django.db import models

class Product(models.Model):
    id_product = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    ingredients = models.TextField()
    stock = models.IntegerField(default=0)
    is_vegan = models.BooleanField(default=False)
    is_vegetarian = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['name']

    def __str__(self):
        return self.name

class Customer(models.Model):
    id_customer = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=200)
    # Relaciones con Wishlist y Cart
    # id_wishlist = models.OneToOneField(Wishlist, on_delete=models.SET_NULL, null=True, blank=True)
    # id_cart = models.OneToOneField(Cart, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return self.name

# Implementar los modelos Wishlist, Review, Cart, ItemCart, PaymentMethod y Order
# siguiendo el diagrama de clases adjunto.