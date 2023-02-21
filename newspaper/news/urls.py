from django.contrib import admin
from django.urls import path, include
from .views import NewsList, upgrade_me_redposts,  delete_me_redpost,  NewsDetail, NewsCreate, ArticleCreate, PostUpdate, PostDelete

urlpatterns = [
    path('posts/', NewsList.as_view(), name='post_list'),
    path('posts/<int:pk>', NewsDetail.as_view(), name='post_detail'),
    path('news/create/', NewsCreate.as_view(), name='post_create'),
    path('articles/create/', ArticleCreate.as_view(), name='post_create'),
    path('news/<int:pk>/edit', PostUpdate.as_view(), name='post_update'),
    path('articles/<int:pk>/edit', PostUpdate.as_view(), name='article_update'),
    path('news/<int:pk>/delete', PostDelete.as_view(), name='news_delete'),
    path('articles/<int:pk>/delete', PostDelete.as_view(), name='article_delete'),
    path('posts/upgrade/', upgrade_me_redposts, name='upgrade_posts'),
    path('post/upgrade/', delete_me_redpost, name='upgrade_posts')
]
