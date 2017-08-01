from phonenumber_field.formfields import PhoneNumberField
from dal.autocomplete import ModelSelect2

from django import forms
from django.utils.translation import ugettext_lazy as _

from book.models import Book
from book.models import BookReading


class BookReadingForm(forms.ModelForm):
    name = forms.CharField(
        label=_('Full Name'),
    )
    phone_number = PhoneNumberField(
        label=_('Phone number')
    )
    city = forms.CharField(
        label=_('City')
    )
    novaposhta_number = forms.CharField(
        label=_('Novaposhta department number')
    )

    class Meta:
        model = BookReading
        fields = ('book', )
        widgets = {
            'book': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(BookReadingForm, self).__init__(*args, **kwargs)
        if request and request.user.is_authenticated():
            self.fields['name'].initial = request.user.get_full_name()
            self.fields['phone_number'].initial = request.user.phone
            self.fields['city'].initial = request.user.city
            self.fields['novaposhta_number'].initial = \
                request.user.novaposhta_number


class AddBookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = (
            'author', 'name', 'description', 'photo', 'category', 'genre',
            'language',
        )
        widgets = {
            'category': ModelSelect2(url='book:category-autocomplete'),
            'genre': ModelSelect2(url='book:genre-autocomplete'),
        }

    def __init__(self, *args, **kwargs):
        super(AddBookForm, self).__init__(*args, **kwargs)
        fields = ['left', 'top', 'width', 'height']
        for field in fields:
            name = 'point_{}'.format(field)
            self.fields[name] = forms.CharField(widget=forms.HiddenInput())

    def get_coords(self):
        data = self.cleaned_data
        return (
            int(data['point_left']),
            int(data['point_top']),
            int(data['point_width']),
            int(data['point_height']),
        )
