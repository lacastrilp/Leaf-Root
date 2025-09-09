from django import forms
from leaf_and_root.catalogo.models import Product, Review


class ProductForm(forms.ModelForm):
    """Formulario para crear/editar productos"""
    class Meta:
        model = Product
        fields = ["name", "description", "price", "stock", "category", "image_url", "nutriscore", "labels"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre del producto"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Descripción"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "stock": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "category": forms.TextInput(attrs={"class": "form-control", "placeholder": "Categoría"}),
            "image_url": forms.URLInput(attrs={"class": "form-control", "placeholder": "URL de la imagen"}),
            "nutriscore": forms.TextInput(attrs={"class": "form-control", "placeholder": "NutriScore (a-e)"}),
            "labels": forms.TextInput(attrs={"class": "form-control", "placeholder": "Etiquetas (ej: vegano, orgánico)"}),
        }


class ReviewForm(forms.ModelForm):
    """Formulario para agregar reseñas a productos"""
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 5}),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Escribe tu reseña..."}),
        }
