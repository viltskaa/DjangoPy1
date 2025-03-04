from django import forms


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

