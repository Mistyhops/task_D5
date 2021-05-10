from django_filters import FilterSet
from django.forms import DateInput
import django_filters

from .models import Post

choices = ['2312', '32435']

class PostFilter(FilterSet):
    time = django_filters.DateFilter(field_name='time', widget=DateInput(attrs={'type': 'date'}), lookup_expr='gt',
                                     label='Позже даты')
    header = django_filters.CharFilter(field_name='header',
                                       lookup_expr='icontains',
                                       label='Заголовок')

    class Meta:
        model = Post
        fields = {
            'author': ['exact'],
        }
