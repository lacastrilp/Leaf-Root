from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from users.models import Customer

class CustomerRegistrationForm(forms.ModelForm):
    """Formulario para registrar un cliente asociado a un usuario del sistema"""
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"})
    )
    password_confirmation = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirm Password"})
    )

    class Meta:
        model = Customer
        fields = ["name", "email", "address", "phone"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Full Name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email Address"}),
            "address": forms.TextInput(attrs={"class": "form-control", "placeholder": "Address"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone Number"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")
        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError("Passwords do not match.")
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
    
class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email Address"})
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "form-control", "placeholder": "Username"})
        self.fields["email"].widget.attrs.update({"class": "form-control", "placeholder": "Email Address"})
        self.fields["password1"].widget.attrs.update({"class": "form-control", "placeholder": "Password"})
        self.fields["password2"].widget.attrs.update({"class": "form-control", "placeholder": "Confirm Password"})

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already registered.")
        return email


class LoginForm(AuthenticationForm):
    """Login form"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Campo unificado: permite ingresar username o email
        self.fields["username"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Username or Email"
        })
        self.fields["password"].widget.attrs.update({"class": "form-control", "placeholder": "Password"})

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name", "email", "address", "phone"]