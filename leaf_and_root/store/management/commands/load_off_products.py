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
    help = "Carga productos en inglés desde Open Food Facts con precios válidos (>0), limpia los existentes y evita duplicados"

    def handle(self, *args, **kwargs):
        # 🧹 Limpiar todos los productos antes de importar nuevos
        self.stdout.write("🧹 Eliminando todos los productos existentes...")
        deleted_count, _ = Product.objects.all().delete()
        self.stdout.write(self.style.WARNING(f"🗑️ {deleted_count} productos eliminados."))

        # Parámetros base de la API
        params = {
            "action": "process",
            "tagtype_0": "labels",
            "tag_contains_0": "contains",
            "tag_0": "vegetarian",
            "sort_by": "unique_scans_n",
            "page_size": 800,
            "json": 1,
        }

        self.stdout.write("📥 Consultando productos desde Open Food Facts (solo inglés)...")
        created_count = 0
        skipped_non_english = 0
        duplicate_fixed = 0

        for page in range(1, 8):  # Hasta 7 páginas (~5600 productos máx.)
            params["page"] = page
            response = requests.get(API_URL, params=params)
            if response.status_code != 200:
                self.stderr.write(f"❌ Error {response.status_code} al consultar la API")
                continue

            data = response.json()
            products = data.get("products", [])

            for p in products:
                # ⚠️ Solo productos en inglés
                lang = p.get("lang") or ""
                languages = p.get("languages_tags", [])
                if lang != "en" and "en" not in languages:
                    skipped_non_english += 1
                    continue

                name = p.get("product_name")
                if not name:
                    continue

                # Evitar nombres duplicados
                clean_name = name.strip()[:255]
                if Product.objects.filter(name=clean_name).exists():
                    clean_name = f"{clean_name} ({random.randint(1000,9999)})"
                    duplicate_fixed += 1

                # Clasificar tipo según etiquetas
                labels = p.get("labels_tags", [])
                if "vegan" in labels:
                    product_type = "vegan"
                elif "vegetarian" in labels:
                    product_type = "vegetarian"
                else:
                    product_type = "plant-based"

                # Asignar precio y stock válidos
                price = assign_price(product_type)
                stock = random.randint(5, 50)

                # Crear producto
                Product.objects.create(
                    name=clean_name,
                    description=p.get("ingredients_text", "No description available."),
                    price=price,
                    stock=stock,
                    category=",".join(p.get("categories_tags", [])[:1]) or "general",
                    image_url=p.get("image_url", None),
                    nutriscore=p.get("nutriscore_grade", None),
                    labels=",".join(labels),
                    type=product_type,
                )
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"✅ {created_count} productos creados en inglés "
                f"({skipped_non_english} ignorados por idioma, {duplicate_fixed} nombres duplicados ajustados)"
            )
        )
