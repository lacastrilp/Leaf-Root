import requests
import random
from django.core.management.base import BaseCommand
from catalogo.models import Product

API_URL = "https://world.openfoodfacts.org/cgi/search.pl"

# Rangos de precio por tipo de producto
price_map = {
    "vegan": (5, 15),
    "vegetarian": (4, 12),
    "plant-based": (3, 10),
}

def assign_price(product_type):
    """Devuelve un precio aleatorio según el tipo de producto"""
    low, high = price_map.get(product_type, (5, 15))
    price = round(random.uniform(low, high), 2)
    return max(price, 1.0)  # nunca permitir precio 0

class Command(BaseCommand):
    help = "Carga productos desde Open Food Facts con precios por tipo (sin dejar precios en 0)"

    def handle(self, *args, **kwargs):
        params = {
            "action": "process",
            "tagtype_0": "labels",
            "tag_contains_0": "contains",
            "tag_0": "plant-based",  # Trae vegan, vegetarian y plant-based
            "sort_by": "unique_scans_n",
            "page_size": 1500,
            "json": 1,
        }

        self.stdout.write("📥 Consultando productos desde Open Food Facts...")
        created_count = 0
        updated_count = 0
        skipped_count = 0

        for page in range(1, 8):  # Hasta 7 páginas (~10k productos máx.)
            params["page"] = page
            response = requests.get(API_URL, params=params)
            if response.status_code != 200:
                self.stderr.write(f"❌ Error {response.status_code} al consultar la API")
                continue

            data = response.json()
            products = data.get("products", [])

            for p in products:
                name = p.get("product_name")
                if not name:
                    continue

                # Clasificar tipo según etiquetas
                labels = p.get("labels_tags", [])
                if "vegan" in labels:
                    product_type = "vegan"
                elif "vegetarian" in labels:
                    product_type = "vegetarian"
                else:
                    product_type = "plant-based"

                # Verificar si el producto ya existe
                existing = Product.objects.filter(name=name[:255]).first()

                # Si ya existe y tiene precio válido (> 0), lo saltamos
                #if existing and existing.price and existing.price > 0:
                #    skipped_count += 1
                #    continue

                # Generar precio válido
                price = assign_price(product_type)
                if not price or price <= 0:
                    price = assign_price("plant-based")

                # Crear o actualizar
                product, created = Product.objects.update_or_create(
                    name=name[:255],
                    defaults={
                        "description": p.get("ingredients_text", "Sin descripción"),
                        "price": price,
                        "stock": 10,
                        "category": ",".join(p.get("categories_tags", [])[:1]) or "general",
                        "image_url": p.get("image_url", None),
                        "nutriscore": p.get("nutriscore_grade", None),
                        "labels": ",".join(labels),
                        "type": product_type,
                    },
                )

                if created:
                    created_count += 1
                else:
                    updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"✅ {created_count} productos creados, "
                f"{updated_count} actualizados, "
                f"{skipped_count} saltados (ya tenían precio > 0)"
            )
        )
