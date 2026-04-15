from django import forms
from .models import Book, Category, Announcement, Journal


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'category', 'cover_color', 'file', 'badge', 'rating', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'cover_color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'badge': forms.Select(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '5'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'emoji', 'color', 'slug']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'emoji': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'body', 'color']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
        }


class JournalForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ['name', 'cover_color', 'year', 'issues_count']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'cover_color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'issues_count': forms.NumberInput(attrs={'class': 'form-control'}),
        }
