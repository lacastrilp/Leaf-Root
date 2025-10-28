from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from catalogo.models import Product, Review
from users.models import Customer


class CustomerRegistrationForm(forms.ModelForm):
    """Formulario para registrar un cliente asociado a un usuario del sistema"""
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Contraseña"})
    )
    password_confirmation = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirma tu contraseña"})
    )


    class Meta:
        model = Customer
        fields = ["name", "email", "address", "phone"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre completo"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Correo electrónico"}),
            "address": forms.TextInput(attrs={"class": "form-control", "placeholder": "Dirección"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Teléfono"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")
        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data

    def save(self, commit=True):
        customer = super().save(commit=False)
        user = User.objects.create_user(
            username=self.cleaned_data["email"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password"],
        )
        customer.user = user
        if commit:
            customer.save()
        return customer


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


class RegisterForm(UserCreationForm):
    """Formulario de registro de usuarios básicos"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Correo electrónico"})
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "form-control", "placeholder": "Nombre de usuario"})
        self.fields["password1"].widget.attrs.update({"class": "form-control", "placeholder": "Contraseña"})
        self.fields["password2"].widget.attrs.update({"class": "form-control", "placeholder": "Repite la contraseña"})


class LoginForm(AuthenticationForm):
    """Formulario de inicio de sesión"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "form-control", "placeholder": "Usuario"})
        self.fields["password"].widget.attrs.update({"class": "form-control", "placeholder": "Contraseña"})

