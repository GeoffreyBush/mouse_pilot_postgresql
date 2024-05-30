from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from website.models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Username"}),
        label="Username",
        required=True,
        min_length=5,
        max_length=20,
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Email"}), label="Email"
    )
    password1 = forms.CharField(
        label="Password",
        min_length=8,
        max_length=20,
        widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        min_length=8,
        max_length=20,
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}),
    )

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):

    # Minimum and maximum lengths for username and password

    class Meta:
        model = CustomUser
        fields = ("username", "email")
