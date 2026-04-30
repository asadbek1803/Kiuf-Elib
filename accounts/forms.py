from django import forms
from .models import Student
from django.contrib.admin.forms import AdminAuthenticationForm

class CustomAdminLoginForm(AdminAuthenticationForm):
    username = forms.CharField(
        label="Login",  # "HEMIS ID" o'rniga "Login"
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'placeholder': 'Login kiriting',
        })
    )
    password = forms.CharField(
        label="Parol",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Parol kiriting',
        })
    )


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
    birth_date = forms.DateField(
        label="Tug'ilgan kun",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'placeholder': 'DD.MM.YYYY'
        })
    )


class StudentAddForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['hemis_id', 'full_name', 'faculty', 'year', 'birth_date']
        widgets = {
            'hemis_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'HEMIS ID'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'To\'liq ism'}),
            'faculty': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fakultet'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Kurs'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class SuperUserAddForm(forms.Form):
    hemis_id = forms.CharField(
        label="Login",
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Login kiriting',
            'autofocus': True
        })
    )
    password = forms.CharField(
        label="Parol",
        max_length=128,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Parolni kiriting'
        })
    )
