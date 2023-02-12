from django_filters import FilterSet, DateFilter, ModelChoiceFilter
from django import forms

from .models import Post, User


class DateInput(forms.DateInput):
    input_type = 'date'


class PostFilter(FilterSet):
    time_in = DateFilter(field_name='time_in', lookup_expr=('gt'), widget=DateInput(), label='Все статьи позже: ')
    author = ModelChoiceFilter(
        field_name='author__user',
        queryset=User.objects.exclude(id=7),
        label='Автор: '
    )

    class Meta:
        model = Post
        fields = {
            'title':['icontains'],
    }
