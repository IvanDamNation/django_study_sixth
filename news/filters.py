from django.forms import DateInput
from django_filters import FilterSet, CharFilter, DateFilter, ModelChoiceFilter
from .models import Post, Author


class PostFilter(FilterSet):
    date = DateFilter(field_name='dateCreation',
                      lookup_expr='gte',
                      label='Create after',
                      widget=DateInput(attrs={'type': 'date'}))
    title = CharFilter(lookup_expr='icontains')
    author = ModelChoiceFilter(queryset=Author.objects.all())
    date.field.error_messages = {'invalid': 'Enter date in format DD.MM.YYYY. Example: 31.12.2020'}
    date.field.widget.attrs = {'placeholder': 'DD.MM.YYYY'}

    class Meta:
        model = Post
        fields = ['date', 'title', 'author']
