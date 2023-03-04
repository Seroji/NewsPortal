import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from ...models import Subscribers, Post, User

from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


def every_week_sending():
    time_from = (datetime.utcnow() + timedelta(hours=3)) - timedelta(weeks=1)
    for user in User.objects.all():
        posts = []
        for subscriber in Subscribers.objects.filter(user_id=user.id):
            for post in Post.objects.filter(postcategory__category_id=subscriber.category_id, time_in__gt=time_from):
                posts.append(post)
        if posts:
            html_content = render_to_string(
                'emails/every_week_sending.html',
                {
                    'name': f"{User.objects.get(pk=user.id).first_name} "
                            f"{User.objects.get(pk=user.id).last_name}",
                    'posts':posts,
                }
            )

            msg = EmailMultiAlternatives(
                subject=f"{User.objects.get(pk=user.id).first_name} "
                        f"{User.objects.get(pk=user.id).last_name}, итоги за неделю",
                from_email='gamexr6@mail.ru',
                to=[f'{User.objects.get(pk=user.id).email}']
            )
            msg.attach_alternative(html_content, 'text/html')
            msg.send()


def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        scheduler.add_job(
            every_week_sending,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="every_week_sending",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="tue", hour="00", minute="00"
            ),
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
