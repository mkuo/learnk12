from django import forms
from django.contrib.auth.forms import UserCreationForm

from user_auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=254, required=True)
    last_name = forms.CharField(max_length=254, required=True)
    email = forms.EmailField(max_length=254, required=True)
    photo = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'photo',
        )


class UpdateProfile(forms.ModelForm):
    first_name = forms.CharField(max_length=254, required=True)
    last_name = forms.CharField(max_length=254, required=True)
    photo = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'photo',
        )
