from django import forms
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField

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
