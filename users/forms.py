from django import forms

from users.models import User


class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'about', 'favourite_book',
            'favourite_author', 'reading_preferences', 'city',
            'novaposhta_number',
        )
        widgets = {
            'about': forms.Textarea(attrs={'rows': 7}),
        }
