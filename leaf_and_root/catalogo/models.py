from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from leaf_and_root.users.models import Customer



class Product(models.Model):
    id_product = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)  # 👈 evitar duplicados exactos
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    stock = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=100, blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    # Extra (puedes usarlos para filtros avanzados en tu tienda)
    nutriscore = models.CharField(max_length=5, blank=True, null=True)
    labels = models.CharField(max_length=255, blank=True, null=True)

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


