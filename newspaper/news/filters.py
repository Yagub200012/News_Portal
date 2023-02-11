from django_filters import FilterSet, CharFilter, DateFilter
from .models import Post
from django import forms


class PostFilter(FilterSet):
    post_title = CharFilter(lookup_expr='iexact')
    post_datetime = DateFilter(widget=forms.DateInput(attrs={'type': 'date'}), lookup_expr='gt')
    cathegory_id__categ_name = CharFilter(lookup_expr='iexact')

    class Meta:
        model = Post
        fields = ['post_title', 'post_datetime', 'cathegory_id__categ_name']
