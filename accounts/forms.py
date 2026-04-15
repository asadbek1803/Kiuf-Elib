from django import forms


class LoginForm(forms.Form):
    hemis_id = forms.CharField(
        label="HEMIS ID",
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'HEMIS ID kiriting',
            'autofocus': True
        })
    )
