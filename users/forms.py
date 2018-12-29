from django import forms
from django.conf import settings
from croppie.fields import CroppieField

from users.models import User


class UserProfileEditForm(forms.ModelForm):

    avatar = CroppieField(
        options={
            'viewport': {
                'width': settings.USER_AVATAR_WIDTH,
                'height': settings.USER_AVATAR_WIDTH,
                'type': 'circle',
            },
            'boundary': {
                'width': settings.USER_AVATAR_WIDTH + 80,
                'height': settings.USER_AVATAR_WIDTH + 80,
            },
            'showZoomer': True,
        },
    )

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'about', 'favourite_book',
            'favourite_author', 'reading_preferences', 'city',
            'novaposhta_number', 'phone', 'avatar',
        )
        widgets = {
            'about': forms.Textarea(attrs={'rows': 7}),
            'phone': forms.TextInput(attrs={'placeholder': '+380'}),
        }


class RegisterForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'password', )
        widgets = {
            'password': forms.PasswordInput(),
        }


class RegisterInviteForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('password', 'email', 'phone', 'fb')
        widgets = {
            'password': forms.PasswordInput()
        }
        labels = {
            'email': "Email",
            'password': "Пароль",
        }
