import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import EmailMultiAlternatives
from news.models import Author, Category, Post, PostCategory, Comment, UserCategory
from django.template.loader import render_to_string
from django.utils import timezone
import datetime


logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
    #  Your job processing logic here...
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


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")



        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="wed", hour="17", minute="04"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()

            logger.info("Scheduler shut down successfully!")