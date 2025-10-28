from django.contrib import admin
from catalogo.models import Product, Review, Wishlist
from django.utils.html import format_html



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id_product", "name", "price", "category", "stock", "nutriscore", "thumbnail")
    list_filter = ("category", "nutriscore", "labels")
    search_fields = ("name", "category", "labels")

    def thumbnail(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" width="50" height="50" style="object-fit:cover; border-radius:4px;" />', obj.image_url)
        return "—"
    thumbnail.short_description = "Imagen"

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("id_wishlist", "customer", "product")
    search_fields = ("customer__name", "product__name")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id_review", "product", "customer", "rating", "approved")
    list_filter = ("approved", "rating")
    search_fields = ("product__name", "customer__name")


# Register your models here.
