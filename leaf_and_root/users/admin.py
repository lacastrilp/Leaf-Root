from django.contrib import admin
from users.models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id_customer", "name", "email", "phone")
    search_fields = ("name", "email")

# Register your models here.
