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
        fields = ('email', 'password', )
        widgets = {
            'password': forms.PasswordInput(),
        }


class RegisterInviteForm(forms.ModelForm):

    password2 = forms.CharField(
        label='Повторіть пароль',
        widget=forms.PasswordInput(),
    )

    class Meta:
        model = User
        fields = ('password', 'email', )
        widgets = {
            'password': forms.PasswordInput()
        }
        labels = {
            'password': 'Пароль',
            'email': "Email"
        }

    def clean_password2(self):
        password2 = self.cleaned_data['password2']
        password = self.cleaned_data['password']
        if password != password2:
            raise forms.ValidationError("Паролі не співпадають")
        return password2
