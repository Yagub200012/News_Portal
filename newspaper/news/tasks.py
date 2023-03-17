from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from news.models import Author, Category, Post, PostCategory, Comment, UserCategory
from django.template.loader import render_to_string
from django.utils import timezone
import datetime


@shared_task
def news_send():
    categories = Category.objects.all()
    for i in categories:
        poluchateli = []
        for j in UserCategory.objects.filter(category_id=i):
            try:
                for p in j:
                    a = str(p.user_id.email)
                    poluchateli.append(a)
            except TypeError:
                a = str(j.user_id.email)
                poluchateli.append(a)

        # отбор новостей по дате
        start_of_week = timezone.now() - datetime.timedelta(days=timezone.now().weekday())
        posts_this_week = Post.objects.filter(post_datetime__gte=start_of_week, cathegory_id=i)

        try:
            for f in posts_this_week:
                subject = f.post_title
                from_email = 'annakim4@yandex.ru'
                to_email = poluchateli

                html_content = render_to_string('email.html', {'post': f})
                msg = EmailMultiAlternatives(subject, '', from_email, to_email)
                msg.attach_alternative(html_content, "text/html")
                msg.send()
        except TypeError:
            subject = posts_this_week[0].post_title
            from_email = 'annakim4@yandex.ru'
            to_email = poluchateli

            html_content = render_to_string('email.html', {'post': posts_this_week})
            msg = EmailMultiAlternatives(subject, '', from_email, to_email)
            msg.attach_alternative(html_content, "text/html")
            msg.send()