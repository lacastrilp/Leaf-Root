from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from .models import Order

class GenerateInvoicePDF(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        return HttpResponse(f"Factura PDF generada para la orden {order.pk}")

# Create your views here.
