from rest_framework import serializers
from django.urls import reverse
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    image_abs_url = serializers.SerializerMethodField()
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id_product",
            "name",
            "description",
            "category",
            "price",
            "stock",
            "image_url",        # URL que ya tienes en tu modelo
            "image_abs_url",    # URL absoluta construida con el request
            "detail_url",       # URL a la vista de detalle
        ]

    def get_image_abs_url(self, obj):
        """
        Convierte image_url en una URL completa con dominio.
        Ejemplo: http://localhost:8000/static/img/x.jpg
        """
        request = self.context.get("request")
        if obj.image_url:
            return request.build_absolute_uri(obj.image_url)
        return None

    def get_detail_url(self, obj):
        """
        URL absoluta hacia la página de detalle del producto.
        """
        request = self.context.get("request")
        url = reverse("product_detail", args=[obj.id_product])
        return request.build_absolute_uri(url)
