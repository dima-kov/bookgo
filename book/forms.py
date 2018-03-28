from phonenumber_field.formfields import PhoneNumberField
from dal.autocomplete import ModelSelect2
from croppie.fields import CroppieField

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.urls import reverse
from django.core.exceptions import ValidationError

from book.models import Book
from book.models import BookReading
from book.models import Genre
from book.models import Category


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
        self.request = request
        super(BookReadingForm, self).__init__(*args, **kwargs)
        if request and request.user.is_authenticated():
            self.fields['full_name'].initial = request.user.get_full_name()
            self.fields['phone'].initial = request.user.phone
            self.fields['city'].initial = request.user.city
            self.fields['novaposhta_number'].initial = \
                request.user.novaposhta_number

    def clean(self):
        cleaned_data = super(BookReadingForm, self).clean()
        if not self.request.user.has_enough_to_read():
            raise ValidationError(_(
                'You have not enough Opportunities to read the book. Please, '
                '<a href="{}">add one book</a> to Bocrok in order to '
                'get 3 new opprtunies!'.format(reverse('book:add'))
            ))
        if self.request.user.has_unfinished_readings():
            raise ValidationError(_(
                'You have already taken one book on the site! Read it '
                'first and turn it back!'
            ))
        if not cleaned_data['book'].available_to_take():
            raise ValidationError(_(
                'This book is currently read by another person. So, '
                'wait for her to retire!'
            ))
        return cleaned_data


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


class CustomCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    option_template_name = 'common/checkbox_option.html'


class BookListFilterForm(forms.Form):
    genre = forms.ModelChoiceField(
        queryset=Genre.objects.all(),
        empty_label=None,
        widget=CustomCheckboxSelectMultiple,
        label=_('Жанр'),
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label=None,
        widget=CustomCheckboxSelectMultiple,
        label=_('Категорія'),
    )
    # language = forms.ChoiceField(
    #     choices=Book.LANGUAGES,
    #     widget=CustomCheckboxSelectMultiple,
    #     label=_('Language'),
    # )


class BookFeedbackForm(forms.ModelForm):
    class Meta:
        model = BookReading
        fields = ['feedback']
        widgets = {
            'feedback': forms.Textarea(attrs={
                'rows': 8,
                'placeholder': _('Say something about book')
            })
        }
