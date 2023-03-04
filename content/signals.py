from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Subscribers, User, PostCategory, Post


@receiver(signal=post_save, sender=PostCategory)
def subscribers_notify(sender, instance, created, **kwargs):
    category_id = instance.category_id
    text = str(Post.objects.get(pk=instance.post_id).text)
    if created:
        for subscriber in Subscribers.objects.filter(category_id=category_id):
            html_content = render_to_string(
                'emails/post_created.html',
                {
                    'name': f"{User.objects.get(pk=subscriber.user_id).first_name} "
                            f"{User.objects.get(pk=subscriber.user_id).last_name}",
                    'text': text,
                    'id':instance.post_id,
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
