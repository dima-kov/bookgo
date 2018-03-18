from django import forms

from book.models import Book


class AddBookForm(forms.ModelForm):

    email = forms.EmailField()

    class Meta:
        model = Book
        fields = ('name', 'author', )
