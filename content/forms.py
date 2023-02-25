from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django import forms

from allauth.account.forms import SignupForm

from .models import Post


class NewsForm(forms.ModelForm):
    title = forms.CharField(
        label='Заголовок',
        widget=forms.TextInput(attrs={'size':100})
    )

    class Meta:
        model = Post
        fields = (
            'author',
            'category',
            'title',
            'text',
        )


class ProfileEditForm(forms.ModelForm):
    username = forms.CharField(max_length=50, label='Имя пользователя')
    email = forms.EmailField(label='Электронная почта')
    first_name = forms.CharField(max_length=50, label='Имя')
    last_name = forms.CharField(max_length=50, label='Фамилия')

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name'
        )


class PasswordEditForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = (
            'password1',
            'password2'
        )


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Электронная почта')
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user

