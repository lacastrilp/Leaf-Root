from django.urls import path
from . import views

urlpatterns = [
    # Facturación
    path("order/<int:order_id>/invoice/", views.GenerateInvoicePDF.as_view(), name="generate_invoice_pdf"),
]
