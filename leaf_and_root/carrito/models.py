from django.db import models
from leaf_and_root.catalogo.models import Product
from leaf_and_root.users.models import Customer


class Cart(models.Model):
    id_cart = models.AutoField(primary_key=True)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f"Carrito de {self.customer.name}"

    def add_product(self, product, quantity=1):
        item, created = ItemCart.objects.get_or_create(cart=self, product=product)
        if not created:
            item.quantity += quantity
            item.save()
        return item

    def total_items(self):
        return self.items.aggregate(total=models.Sum('quantity'))['total'] or 0 # type: ignore
    
    def total_price(self):
        return sum(item.get_subtotal() for item in self.items.all()) # type: ignore


class ItemCart(models.Model):
    id_itemcart = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")  # 👈 importante
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Item del Carrito"
        verbose_name_plural = "Items del Carrito"
        unique_together = ("product", "cart")  # evita duplicados

    def __str__(self):
        return f"{self.quantity}x {self.product.name} en carrito de {self.cart.customer.name}"

    def get_subtotal(self):
        return self.quantity * self.product.price


# Create your models here.
