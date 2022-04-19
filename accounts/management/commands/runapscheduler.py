import logging
from datetime import datetime

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from news.models import Category, Post

logger = logging.getLogger(__name__)


# Weekly subscription email sending job
def news_sender():
    print()
    print()
    print()
    print()
    print('===================================Sending check!===================================')
    print()
    print()

    # Get all objects from model 'category'
    for category in Category.objects.all():

        # List for news + paths
        news_from_each_category = []

        # Check week number
        week_number_last = datetime.now().isocalendar()[1] - 1

        # Get pk and place in filter. Also filter with week number
        for news in Post.objects.filter(category_id=category.id,
                                        dateCreation__week=week_number_last).values('pk',
                                                                                    'title',
                                                                                    'dateCreation',
                                                                                    'category_id__name'):
            # Reformat date
            date_format = news.get("dateCreation").strftime("%m/%d/%Y")

            # Make object with field + date + path of news
            new = (f' http://127.0.0.1:8000/news/{news.get("pk")}, {news.get("title")}, '
                   f'Category: {news.get("category_id__name")}, Date creation: {date_format}')

            # Each object place to the list
            news_from_each_category.append(new)

        # Kind of frontend of mail
        print()
        print('+++++++++++++++++++++++++++++', category.name, '++++++++++++++++++++++++++++++++++++++++++++')
        print()
        print("List of email recievers: ", category.name, '( id:', category.id, ')')

        # Containment for info about subscribers
        subscribers = category.subscribers.all()

        # For testing and debugging
        print('Sending to: ')
        for qaz in subscribers:
            print(qaz.email)

        print()
        print()

        # Cycle for body (template) of mail to subscribers
        for subscriber in subscribers:
            # Another kind of frontend
            print('____________________________', subscriber.email, '___________________________________')
            print()
            print('Mail sent to the: ', subscriber.email)
            html_content = render_to_string(
                'sender.html', {'user': subscriber,
                                'text': news_from_each_category,
                                'category_name': category.name,
                                'week_number_last': week_number_last})

            msg = EmailMultiAlternatives(
                subject=f'Hello, {subscriber.username}, news of the week in your feed!',
                from_email='fortestapps@yandex.ru',
                to=[subscriber.email]
            )

            msg.attach_alternative(html_content, 'text/html')
            print()

            # For testing purposes
            # print(html_content)

            # Uncomment this to work
            msg.send()


# def my_job():
#     pass
#     # Your job processing logic here...
#     print('Hello from job!')


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            news_sender,
            trigger=CronTrigger(second="*/10"),  # Every 10 seconds
            id="news_sender",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'news_sender'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
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
