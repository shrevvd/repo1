from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year', 'isbn']
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Введите название книги'
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Укажите автора или авторов'
            }),
            'publication_year': forms.NumberInput(attrs={
                'class': 'form-control', 
                'min': '1',
                'placeholder': 'Например: 2026'
            }),
            'isbn': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Например: 978-3-16-148410-0'
            }),
        }
