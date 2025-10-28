from django.urls import path
from . import views

urlpatterns = [
    # Facturación
    path("order/<int:order_id>/invoice/", views.GenerateInvoicePDF.as_view(), name="generate_invoice_pdf"),
    path("checkout/review/", views.checkout_review, name="checkout_review"),
    path("checkout/finalize/", views.checkout_finalize, name="checkout_finalize"),
    path("my-orders/", views.my_orders, name="my_orders"),

    
]
