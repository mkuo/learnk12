from datetime import date

from django import forms
from django.contrib.auth.forms import UserCreationForm

from user_auth.models import User


def birth_validator(birth_date):
    date_today = date.today().year
    res = date_today - birth_date.year
    if not res >= 18:
        raise forms.ValidationError("You must be at least 18 or older to register on this page")


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=254, required=True)
    last_name = forms.CharField(max_length=254, required=True)
    email = forms.EmailField(max_length=254, required=True)
    birth_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}),
                                 required=True, validators=[birth_validator, ])
    photo = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'birth_date', 'photo',
        )


class UpdateProfile(forms.ModelForm):
    first_name = forms.CharField(max_length=254, required=True)
    last_name = forms.CharField(max_length=254, required=True)
    birth_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}),
                                 required=True, validators=[birth_validator, ])
    photo = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'birth_date', 'photo',
        )
