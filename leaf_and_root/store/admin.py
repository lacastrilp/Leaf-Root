from django.contrib import admin
from .models import Product, Category, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "category", "created_at")
    list_filter = ("category", "created_at")
    search_fields = ("name", "category__name")
    ordering = ("-created_at",)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "created_at", "updated_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__username", "status")
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product", "quantity", "price")
    search_fields = ("order__id", "product__name")
