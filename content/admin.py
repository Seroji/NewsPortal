from django.contrib import admin
from .models import Post, Category, Author, PostCategory, Comment, Subscribers

admin.site.register(Author)
admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Subscribers)
