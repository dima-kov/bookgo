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
from users.models import User


class BookReadingForm(forms.ModelForm):
    class Meta:
        model = BookReading
        fields = ('book', 'fb', 'full_name',)
        widgets = {
            'book': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        self.user = request.user
        super(BookReadingForm, self).__init__(*args, **kwargs)
        if request:
            if self.user.fb is not None:
                self.fields.pop('fb')

    def clean(self):
        cleaned_data = super(BookReadingForm, self).clean()

        if self.user.has_unfinished_readings():
            raise ValidationError(_(
                'Ви зараз читаєте іншу книгу, спершу поверніть її, а потім візьміть цю'
            ))

        if not cleaned_data['book'].available_to_exchange():
            raise ValidationError(_(
                'Цю книгу поточно зараз хтось уже читає, виберіть іншу'
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
            'author', 'name', 'description', 'publisher', 'publishing_year',
            'amazon_link', 'pages', 'photo', 'category', 'genre', 'language',
        )
        widgets = {
            'author': forms.TextInput(attrs={'placeholder': _('Автор')}),
            'name': forms.TextInput(attrs={'placeholder': _('Назва')}),
            'publisher': forms.TextInput(attrs={'placeholder': _('Видавництво')}),
            'pages': forms.TextInput(attrs={'placeholder': _('К-сть сторінок')}),
            'amazon_link': forms.URLInput(attrs={'placeholder': _('Посилання на Amazon')}),
            'publishing_year': forms.NumberInput(attrs={'placeholder': _('Рік видавництва')}),

            'category': ModelSelect2(url='book:category-autocomplete'),
            'genre': ModelSelect2(url='book:genre-autocomplete'),
            'description': forms.Textarea(attrs={
                'rows': 12,
                'placeholder': 'Про що ця книга? Чи сподобалась вона вам? Чому?',
            }),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(AddBookForm, self).__init__(*args, **kwargs)
        if self.request and not self.request.user.is_authenticated:
            self.fields['email'] = forms.EmailField(label="Ваш email")


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
