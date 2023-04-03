from django.contrib import admin
from .models import Post, Category, Author, PostCategory, Comment, Subscribers


def delete_all_rating(modeladmin, request, queryset):
    queryset.update(rating=0)
delete_all_rating.short_description = 'Обнулить рейтинг'


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'type', 'Category','title', 'text', 'rating')
    list_filter = ('author', 'time_in')
    search_fields = ('title', 'author__user__username')
    actions = [delete_all_rating]

    def Category(self, obj):
        category_id = PostCategory.objects.get(post_id=obj.id).category_id
        category = Category.objects.get(pk=category_id)
        return category.category


admin.site.register(Author)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Subscribers)
