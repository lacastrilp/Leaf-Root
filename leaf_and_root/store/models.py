from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    id_customer = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return self.name


class Product(models.Model):
    id_product = models.AutoField(primary_key=True)  # 👈 lo defines explícito
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to="products/", blank=True, null=True)

    def __str__(self):
        return self.name


class Wishlist(models.Model):
    id_wishlist = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="wishlists")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="wishlisted_by")

    class Meta:
        verbose_name = "Lista de Deseos"
        verbose_name_plural = "Listas de Deseos"
        unique_together = ("customer", "product")

    def __str__(self):
        return f"Wishlist de {self.customer.name}"


class Review(models.Model):
    id_review = models.AutoField(primary_key=True)
    comment = models.TextField()
    rating = models.IntegerField()
    approved = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Reseña"
        verbose_name_plural = "Reseñas"

    def __str__(self):
        return f"Reseña de {self.customer.name} para {self.product.name}"


class Cart(models.Model):
    id_cart = models.AutoField(primary_key=True)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Carrito de Compras"
        verbose_name_plural = "Carritos de Compras"

    def __str__(self):
        return f"Carrito de {self.customer.name}"


class ItemCart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Item del Carrito"
        verbose_name_plural = "Items del Carrito"

    def __str__(self):
        return f"{self.quantity}x {self.product.name} en carrito de {self.cart.customer.name}"

    def get_subtotal(self):
        return self.quantity * self.product.price


class PaymentMethod(models.Model):
    id_payment_method = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50)
    card_number = models.CharField(max_length=16)  # ⚠️ debería tokenizarse
    expiration_date = models.CharField(max_length=5)
    security_code = models.CharField(max_length=3)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Método de Pago"
        verbose_name_plural = "Métodos de Pago"

    def __str__(self):
        return f"Tarjeta de {self.customer.name} - ****{self.card_number[-4:]}"


class Order(models.Model):
    STATUS_CHOICES = [
        ("Pendiente", "Pendiente"),
        ("Pagado", "Pagado"),
        ("Cancelada", "Cancelada"),
    ]

    id_order = models.AutoField(primary_key=True)
    order_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Pendiente")
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Orden"
        verbose_name_plural = "Órdenes"

    def __str__(self):
        return f"Orden #{self.id_order} - {self.customer.name}"

    def cancel(self):
        from .services import cancel_order
        return cancel_order(self.id_order)

    def process_payment(self):
        from .services import process_order_payment
        return process_order_payment(self.id_order)
