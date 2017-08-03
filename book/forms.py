from phonenumber_field.formfields import PhoneNumberField
from dal.autocomplete import ModelSelect2
from croppie.fields import CroppieField

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from book.models import Book
from book.models import BookReading


class BookReadingForm(forms.ModelForm):
    phone = PhoneNumberField(
        label=_('Phone number')
    )

    class Meta:
        model = BookReading
        fields = ('book', 'full_name', 'phone', 'city', 'novaposhta_number', )
        widgets = {
            'book': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(BookReadingForm, self).__init__(*args, **kwargs)
        if request and request.user.is_authenticated():
            self.fields['full_name'].initial = request.user.get_full_name()
            self.fields['phone'].initial = request.user.phone
            self.fields['city'].initial = request.user.city
            self.fields['novaposhta_number'].initial = \
                request.user.novaposhta_number


class AddBookForm(forms.ModelForm):

    photo = CroppieField(
        options={
            'viewport': {
                'width': settings.BOOK_CARD_IMAGE_WIDTH,
                'height': settings.BOOK_CARD_IMAGE_HEIGHT,
            },
            'boundary': {
                'width': settings.BOOK_CARD_IMAGE_WIDTH + 80,
                'height': settings.BOOK_CARD_IMAGE_HEIGHT + 80,
            },
            'showZoomer': True,
        },
    )

    class Meta:
        model = Book
        fields = (
            'author', 'name', 'description', 'photo', 'category', 'genre',
            'language',
        )
        widgets = {
            'description': forms.Textarea(attrs={'rows': 12}),
            'category': ModelSelect2(url='book:category-autocomplete'),
            'genre': ModelSelect2(url='book:genre-autocomplete'),
        }
        help_texts = {
            'description': _(
                'Tell us a bit about this book.'
                'Do you like it? Why? What feelings did it caused?'
            ),
        }
