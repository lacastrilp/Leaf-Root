from django.contrib import admin
from ordenes.models import Order, PaymentMethod




@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ("id_payment_method", "customer", "type", "card_number", "expiration_date")
    search_fields = ("customer__name", "type")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id_order", "customer", "status", "order_date")
    list_filter = ("status", "order_date")
    search_fields = ("customer__name", "status")
    
# Register your models here.
