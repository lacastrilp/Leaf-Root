from django.contrib import admin
from carrito.models import Cart, ItemCart



class ItemCartInline(admin.TabularInline):
    model = ItemCart
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id_cart", "customer")
    inlines = [ItemCartInline]


# Register your models here.
