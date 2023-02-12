from django import forms

from .models import Post


class NewsForm(forms.ModelForm):
    article = 'A'
    news = 'N'
    TYPES = [
        (article, 'Статья'),
        (news, 'Новость')
    ]

    type = forms.ChoiceField(
        choices=TYPES,
        label='Тип записи'
    )

    title = forms.CharField(
        label='Заголовок',
        widget=forms.TextInput(attrs={'size':100})
    )

    class Meta:
        model = Post
        fields = [
            'type',
            'author',
            'category',
            'title',
            'text']
