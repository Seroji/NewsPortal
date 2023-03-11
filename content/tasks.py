from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from celery import shared_task

from datetime import datetime, timedelta

from .models import Post, PostCategory, Subscribers, User


@shared_task
def notify_subscribers(post):
    post_id = post
    category_id = PostCategory.objects.get(post_id=post_id).category_id
    text = str(Post.objects.get(pk=post_id).text)
    for subscriber in Subscribers.objects.filter(category_id=category_id):
        html_content = render_to_string(
            'emails/post_created.html',
            {
                'name':f"{User.objects.get(pk=subscriber.user_id).first_name} "
                        f"{User.objects.get(pk=subscriber.user_id).last_name}",
                'text':text,
                'id':post_id,
            }
        )

        msg = EmailMultiAlternatives(
            subject=f"{User.objects.get(pk=subscriber.user_id).first_name} "
                    f"{User.objects.get(pk=subscriber.user_id).last_name}, взгляните!",
            from_email='gamexr6@mail.ru',
            to=[f'{User.objects.get(pk=subscriber.user_id).email}']
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()


@shared_task
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
