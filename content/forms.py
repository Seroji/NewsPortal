from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.core.exceptions import ValidationError
from django import forms

from allauth.account.forms import LoginForm

from .models import Post, Author, Category


class NewsCreateForm(forms.ModelForm):
    title = forms.CharField(label='Заголовок', widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}))
    text = forms.CharField(label='Содержание', widget=forms.Textarea(attrs={'class': 'form-control', 'type': 'text', 'rows':'5'}))
    category = forms.ChoiceField(
                                choices=[(category.pk, category) for category in Category.objects.all()], 
                                 widget=forms.Select(attrs={'class': 'form-select form-select-sm'}))

    class Meta:
        model = Post
        fields = (
            'category',
            'title',
            'text',
        )


class NewsEditForm(forms.ModelForm):
    title = forms.CharField(
        label='Заголовок',
        widget=forms.TextInput(attrs={'size': 100})
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
    username = forms.CharField(max_length=50, label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}))
    email = forms.EmailField(label='Электронная почта', widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'email'}))
    first_name = forms.CharField(max_length=50, label='Имя', widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}))
    last_name = forms.CharField(max_length=50, label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}))

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
        )


class PasswordEditForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))

    class Meta:
        model = User
        fields = (
            'old_password',
            'new_password1',
            'new_password2',
        )


class UserRegisterForm(UserCreationForm):
    email = forms.CharField(label='Электронная почта', widget=forms.EmailInput(attrs={'class': 'form-control', 'type': 'email', 'style': 'width:500px'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'style': 'width:500px'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'style': 'width:500px'}))
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'style': 'width:500px'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'style': 'width:500px'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'style': 'width:500px'}))

    def clean(self):
        super().clean()
        register_email = self.cleaned_data.get('email')
        if User.objects.filter(email=register_email):
            raise ValidationError("Пользователь с таким E-mail уже существует!")
        else:
            return self.cleaned_data
        

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
    

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget.attrs.update({
            'class': 'form-control mx-auto',
            'type': 'email',
            'style':'width:500px',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control mx-auto',
            'type': 'password',
            'style':'width:500px',
        })
        