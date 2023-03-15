from django.contrib import admin
from django.urls import path, include
from .views import NewsList, AccountDate, upgrade_me, NewsDetail, NewsCreate, ArticleCreate, PostUpdate, PostDelete, subscription1, subscription2, subscription3, subscription4

urlpatterns = [
    path('', NewsList.as_view(), name='post_list'),
    path('<int:pk>', NewsDetail.as_view(), name='post_detail'),
    path('news/create/', NewsCreate.as_view(), name='post_create'),
    path('articles/create/', ArticleCreate.as_view(), name='post_create'),
    path('news/<int:pk>/edit', PostUpdate.as_view(), name='post_update'),
    path('articles/<int:pk>/edit', PostUpdate.as_view(), name='article_update'),
    path('news/<int:pk>/delete', PostDelete.as_view(), name='news_delete'),
    path('articles/<int:pk>/delete', PostDelete.as_view(), name='article_delete'),
    path('personaldata/upgrade/', upgrade_me, name='upgrade'),
    path('personaldata/', AccountDate.as_view(), name='personal.data'),
    path('personaldata/subscribe1/', subscription1, name='subscription_path1'),
    path('personaldata/subscribe2/', subscription2, name='subscription_path2'),
    path('personaldata/subscribe3/', subscription3, name='subscription_path3'),
    path('personaldata/subscribe4/', subscription4, name='subscription_path4'),]
