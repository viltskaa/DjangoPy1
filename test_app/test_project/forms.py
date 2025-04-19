from django import forms

from .models import Author


class TestForm(forms.Form):
    text_field = forms.CharField(
        label="Тестовое поле ввода",
        max_length=63,
        min_length=3,
        required=True
    )

    age_field = forms.IntegerField(
        label="Age",
        min_value=14,
        max_value=90,
        required=True
    )

    password_field = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        max_length=32,
        min_length=8,
        required=True
    )


class BookForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        min_length=5,
        required=True
    )

    count_pages = forms.IntegerField(
        min_value=1,
    )

    author = forms.ModelChoiceField(queryset=Author.objects.all())


class SignUpForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
