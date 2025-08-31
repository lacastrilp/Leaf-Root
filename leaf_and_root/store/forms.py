from django import forms
from django.contrib.auth.models import User
from .models import Customer


class CustomerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirmation = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ["name", "email", "address", "phone"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")
        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data

    def save(self, commit=True):
        customer = super().save(commit=False)
        try:
            user = User.objects.create_user(
                username=self.cleaned_data["email"],
                email=self.cleaned_data["email"],
                password=self.cleaned_data["password"],
            )
            customer.user = user
            if commit:
                customer.save()
        except Exception as e:
            raise forms.ValidationError(f"Error creando el usuario: {e}")
        return customer
