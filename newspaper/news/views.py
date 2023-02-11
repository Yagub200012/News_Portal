from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from .models import Post
from datetime import datetime
from .filters import PostFilter
from .forms import PostForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


class NewsList(ListView):
    model = Post
    ordering = '-post_datetime'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context


class NewsDetail(DetailView):
    model = Post
    ordering = '-post_datetime'
    template_name = 'new.html'
    context_object_name = 'new'


class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        new = form.save(commit=False)
        new.post_format = 'NW'
        new.author_id_id = 1
        return super().form_valid(form)


class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        new = form.save(commit=False)
        new.post_format = 'AR'
        new.author_id_id = 1
        return super().form_valid(form)


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_update.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
