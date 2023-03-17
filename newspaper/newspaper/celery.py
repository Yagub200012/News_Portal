import os
from celery import Celery
from celery.schedules import crontab
from news.tasks import news_send

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from news.models import Author, Category, Post, PostCategory, Comment, UserCategory
from django.template.loader import render_to_string
from django.utils import timezone
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newspaper.settings')


app = Celery('newspaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'task': 'news_send',
        'schedule': crontab(),
        'args': (),
    },
}
