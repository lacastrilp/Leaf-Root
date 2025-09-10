import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from carrito.models import Product
# Rangos de precio por tipo
price_map = {
    "vegan": (5, 15),
    "vegetarian": (4, 12),
    "plant-based": (3, 10),
    "general": (5, 15),  # fallback
}

def assign_price(product_type):
    """Devuelve un precio aleatorio según el tipo de producto"""
    return round(random.uniform(*price_map.get(product_type, (5, 15))), 2)

class Command(BaseCommand):
    help = "Rellena los precios vacíos o en 0 de los productos existentes"

    def handle(self, *args, **kwargs):
        products = Product.objects.filter(price__isnull=True) | Product.objects.filter(price=0)
        count = products.count()

        if count == 0:
            self.stdout.write(self.style.SUCCESS("🎉 No hay productos con price=0"))
            return

        updated = 0
        for product in products:
            product.price = Decimal(str(assign_price(getattr(product, "type", "general"))))
            product.save(update_fields=["price"])
            updated += 1
            updated += 1

        self.stdout.write(self.style.SUCCESS(f"✅ {updated} productos actualizados con nuevo precio"))
