from django import forms


from users.models import User


class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'about', 'favourite_book',
            'favourite_author', 'reading_preferences', 'city',
            'novaposhta_number', 'phone',
        )
        widgets = {
            'about': forms.Textarea(attrs={'rows': 7}),
            'phone': forms.TextInput(attrs={'placeholder': '+380'}),
        }


class RegisterForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('password', 'username', )
        widgets = {
            'password': forms.PasswordInput(),
        }
