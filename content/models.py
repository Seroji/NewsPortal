from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.core.validators import ValidationError

from datetime import datetime, timedelta


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    @receiver(post_save, sender=User)
    def create_user_author(sender, instance, created, **kwargs):
        if created:
            Author.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_author(sender, instance, **kwargs):
        instance.author.save()

    def __str__(self):
        return f"{self.user.get_username()}"

    def update_rating(self, value):
        if value == self.rating:
            value = 0
            for i in Post.objects.filter(author=self.id).values('rating'):
                value += (i.get('rating') * 3)
            for i in Comment.objects.filter(author=self.id).values('rating'):
                value += i.get('rating')
            for i in Comment.objects.filter(post__author=self.id).values('rating'):
                value += i.get('rating')
            self.rating = value
            self.save()
        else:
            pass


class Category(models.Model):
    category = models.CharField(max_length=50, unique=True)
    user = models.ManyToManyField(User, through='Subscribers')

    def __str__(self):
        return f"{self.category.title()}"


class Post(models.Model):
    article = 'A'
    news = 'N'
    TYPES = [
        (article, 'Статья'),
        (news, 'Новость')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=2,
                                choices=TYPES,
                                default=article)
    time_in = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.TextField(default='Заголовок')
    text = models.TextField(default='Содержание')
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1 if self.rating else self.rating
        self.save()

    def preview(self):
        return self.text[:125] + '...'

    def __str__(self):
        return f"{self.title} {self.text[:20]}..."

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        today = datetime.utcnow() + timedelta(hours=3)
        user_records = Post.objects.filter(author_id=self.author_id,
                                           time_in__day=today.day,
                                           time_in__month=today.month).count()
        if user_records >= 3:
            raise ValidationError
        else:
            super().save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    text = models.TextField(default='Комментарий')
    time_in = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1 if self.rating else self.rating
        self.save()


class Subscribers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
