from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Subscribers, User, PostCategory, Post


# @receiver(signal=m2m_changed, sender=Post.category.through)
# def subscribers_notify(instance, action, **kwargs):
#     if action == 'post_add':
#         print('!!!!!!!!!!!!1')
#         # category_id = instance.category
#         # text = str(instance.text)
#         # for subscriber in Subscribers.objects.filter(category_id=category_id):
#         #     html_content = render_to_string(
#         #         'emails/post_created.html',
#         #         {
#         #             'name': f"{User.objects.get(pk=subscriber.user_id).first_name} "
#         #                     f"{User.objects.get(pk=subscriber.user_id).last_name}",
#         #             'text': text,
#         #             'id':instance.id,
#         #         }
#         #     )
#         #
#         #     msg = EmailMultiAlternatives(
#         #         subject=f"{User.objects.get(pk=subscriber.user_id).first_name} "
#         #                 f"{User.objects.get(pk=subscriber.user_id).last_name}, взгляните!",
#         #         from_email='gamexr6@mail.ru',
#         #         to=[f'{User.objects.get(pk=subscriber.user_id).email}']
#         #     )
#         #     msg.attach_alternative(html_content, 'text/html')
#         #     msg.send()


# @receiver(signal=post_save, sender=PostCategory)
# def subscribers_notify(instance, created, **kwargs):
#     category_id = instance.category_id
#     text = str(Post.objects.get(pk=instance.post_id).text)
#     if created:
#         for subscriber in Subscribers.objects.filter(category_id=category_id):
#             html_content = render_to_string(
#                 'emails/post_created.html',
#                 {
#                     'name': f"{User.objects.get(pk=subscriber.user_id).first_name} "
#                             f"{User.objects.get(pk=subscriber.user_id).last_name}",
#                     'text': text,
#                     'id':instance.post_id,
#                 }
#             )
#
#             msg = EmailMultiAlternatives(
#                 subject=f"{User.objects.get(pk=subscriber.user_id).first_name} "
#                         f"{User.objects.get(pk=subscriber.user_id).last_name}, взгляните!",
#                 from_email='gamexr6@mail.ru',
#                 to=[f'{User.objects.get(pk=subscriber.user_id).email}']
#             )
#             msg.attach_alternative(html_content, 'text/html')
#             msg.send()
