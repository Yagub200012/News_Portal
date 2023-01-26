from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post
from datetime import datetime

class NewsList(ListView):
    model = Post
    ordering = '-post_datetime'
    template_name = 'news.html'
    context_object_name = 'news'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = None
        return context

class NewsDetail(DetailView):
    model = Post
    ordering = '-post_datetime'
    template_name = 'new.html'
    context_object_name = 'new'
