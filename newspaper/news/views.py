from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.views.generic.base import View
from .models import Post, Author, UserCategory, Category
from datetime import datetime
from .filters import PostFilter
from .forms import PostForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.http import HttpResponse

from .tasks import hello


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
        # context['is_not_premium'] = not self.request.user.groups.filter(name='authors').exists()
        # context['is_common'] = self.request.user.groups.filter(name='common').exists()
        return context

    def get(self, request):
        hello.delay()
        return HttpResponse('Hello!')


class NewsDetail(DetailView):
    model = Post
    ordering = '-post_datetime'
    template_name = 'new.html'
    context_object_name = 'new'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['is_not_premium'] = not self.request.user.groups.filter(name='authors').exists()
        # context['is_common'] = self.request.user.groups.filter(name='common').exists()
        return context


class NewsCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = 'news.add_post'

    def form_valid(self, form):
        new = form.save(commit=False)
        new.post_format = 'NW'
        new.author_id_id = Author.objects.get(user_id=self.request.user).id
        new.save()

        categories = form.cleaned_data.get('cathegory_id')
        poluchateli = []
        for i in categories:
            for j in UserCategory.objects.filter(category_id = i):
                try:
                    for p in j:
                        a = str(p.user_id.email)
                        poluchateli.append(a)
                except TypeError:
                    a = str(j.user_id.email)
                    poluchateli.append(a)
        subject = new.post_title
        from_email = 'annakim4@yandex.ru'
        to_email = poluchateli

        html_content = render_to_string('email.html', {'post': new})
        msg = EmailMultiAlternatives(subject, '', from_email, to_email)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_premium'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class ArticleCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = 'news.add_post'

    def form_valid(self, form):
        new = form.save(commit=False)
        new.post_format = 'AR'
        new.author_id_id = Author.objects.get(user_id=self.request.user).id
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_premium'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class PostUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_update.html'
    permission_required = 'news.change_post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_premium'] = not self.request.user.groups.filter(name='authors').exists()
        post_id = str(self.request).split('/')[-2]
        post_author_id = Post.objects.get(id=post_id).author_id_id
        user_id = Author.objects.get(user_id_id=self.request.user.id).id
        if post_author_id == user_id:
            context['user_is_author'] = True
        else:
            context['user_is_author'] = False
        return context


class PostDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
    permission_required = 'news.delete_post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_premium'] = not self.request.user.groups.filter(name='authors').exists()
        post_id = str(self.request).split('/')[-2]
        post_author_id = Post.objects.get(id=post_id).author_id_id
        user_id = Author.objects.get(user_id_id=self.request.user.id).id
        if post_author_id == user_id:
            context['user_is_author'] = True
        else:
            context['user_is_author'] = False
        return context


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
        author = Author.objects.create(user_id=user)
        author.save()
    return redirect('/personaldata')


class AccountDate(LoginRequiredMixin, View):
    template_name = 'account_data.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def get_context_data(self):
        context = {}
        context['is_not_premium'] = not self.request.user.groups.filter(name='authors').exists()
        context['username'] = self.request.user.username
        context['email'] = self.request.user.email
        user = self.request.user
        context['policy_exists'] = UserCategory.objects.filter(user_id=user,
                                                               category_id=(Category.objects.get(id=1))).exists()
        context['crime_exists'] = UserCategory.objects.filter(user_id=user,
                                                              category_id=(Category.objects.get(id=2))).exists()
        context['technologists_exists'] = UserCategory.objects.filter(user_id=user,
                                                                      category_id=(Category.objects.get(id=3))).exists()
        context['sport_exists'] = UserCategory.objects.filter(user_id=user,
                                                              category_id=(Category.objects.get(id=4))).exists()
        return context


@login_required
def subscription1(request):
    user = request.user
    if not UserCategory.objects.filter(user_id=user, category_id=(Category.objects.get(id=1))).exists():
        uscat = UserCategory.objects.create(user_id=user, category_id=(Category.objects.get(id=1)))
        uscat.save()
    return redirect('/personaldata')


@login_required
def subscription2(request):
    user = request.user
    if not UserCategory.objects.filter(user_id=user, category_id=(Category.objects.get(id=2))).exists():
        uscat = UserCategory.objects.create(user_id=user, category_id=(Category.objects.get(id=2)))
        uscat.save()
    return redirect('/personaldata')


@login_required
def subscription3(request):
    user = request.user
    if not UserCategory.objects.filter(user_id=user, category_id=(Category.objects.get(id=3))).exists():
        uscat = UserCategory.objects.create(user_id=user, category_id=(Category.objects.get(id=3)))
        uscat.save()
    return redirect('/personaldata')


@login_required
def subscription4(request):
    user = request.user
    if not UserCategory.objects.filter(user_id=user, category_id=(Category.objects.get(id=4))).exists():
        uscat = UserCategory.objects.create(user_id=user, category_id=(Category.objects.get(id=4)))
        uscat.save()
    return redirect('/personaldata')
