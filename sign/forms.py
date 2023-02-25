from django.contrib.auth.models import User
from django import forms


class ProfileForm(forms.ModelForm):
    class UpdateUserForm(forms.ModelForm):
        username = forms.CharField(max_length=50, label='Имя пользователя')
        email = forms.EmailField(label='Электронная почта')
        password1 = forms.PasswordInput()

        class Meta:
            model = User
            fields = (
                'username',
                'email',
                'password1',
                'password2'
            )


