from django import forms

from .models import Post


class NewsForm(forms.ModelForm):
    title = forms.CharField(
        label='Заголовок',
        widget=forms.TextInput(attrs={'size':100})
    )

    class Meta:
        model = Post
        fields = [
            'author',
            'category',
            'title',
            'text']


class ArticleForm(forms.ModelForm):
    title = forms.CharField(
        label='Заголовок',
        widget=forms.TextInput(attrs={'size': 100})
    )

    class Meta:
        model = Post
        fields = [
            'author',
            'category',
            'title',
            'text']