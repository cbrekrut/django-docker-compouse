from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm

class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "id": "login-email",
            "placeholder": "Введите email"
        })
    )
    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "id": "login-password",
            "placeholder": "Введите пароль"
        })
    )

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "id": "reg-email",
            "placeholder": "Введите email"
        })
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "id": "reg-password",
            "placeholder": "Введите пароль"
        })
    )
    password2 = forms.CharField(
        label="Подтвердите пароль",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "id": "reg-password2",
            "placeholder": "Повторите пароль"
        })
    )

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email
    
class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Старый пароль",
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'})
    )
    new_password1 = forms.CharField(
        label="Новый пароль",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'})
    )
    new_password2 = forms.CharField(
        label="Подтвердите новый пароль",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'})
    )