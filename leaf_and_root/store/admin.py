from django.contrib import admin
from .models import Customer, Product, Wishlist, Review, Cart, ItemCart, PaymentMethod, Order


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id_customer", "name", "email", "phone")
    search_fields = ("name", "email")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id_product", "name", "price", "category", "stock")
    list_filter = ("category",)
    search_fields = ("name", "category")


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("id_wishlist", "customer", "product")
    search_fields = ("customer__name", "product__name")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id_review", "product", "customer", "rating", "approved")
    list_filter = ("approved", "rating")
    search_fields = ("product__name", "customer__name")


class ItemCartInline(admin.TabularInline):
    model = ItemCart
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id_cart", "customer")
    inlines = [ItemCartInline]


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ("id_payment_method", "customer", "type", "card_number", "expiration_date")
    search_fields = ("customer__name", "type")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id_order", "customer", "status", "order_date")
    list_filter = ("status", "order_date")
    search_fields = ("customer__name", "status")
    