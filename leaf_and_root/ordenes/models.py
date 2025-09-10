from django.db import models
from carrito.models import Cart
from users.models import Customer



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


# Create your models here.
